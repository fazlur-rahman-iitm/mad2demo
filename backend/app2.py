
from flask import Flask, request, jsonify

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash # module for password hashing

from flask_cors import CORS

from datetime import datetime, timedelta

from flask_migrate import Migrate


app = Flask(__name__) # instance of the flask app

CORS(app, origins='*') # cors configuration

# database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mad2db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

migrate = Migrate(app,db) # database migration setup 

# migration commands
# flask db init
# flask db migrate -m "migration message"
# flask db upgrade

# flask jwt configuration
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'music@mad2'  # change the secret code as u wish


################## Models ##################

class User(db.Model):
    __tablename__ = 'user' 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(1000))
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))
    last_login = db.Column(db.DateTime)

    role = db.Column(db.String())  # role attribute will distinguish between different type of users
    flagged = db.Column(db.Boolean, default=False)
    
    # one to one with Artist
    artist = db.relationship('Artist', backref='user', lazy=True, uselist=False, cascade='all, delete')
    # one to one is same as one to many except the uselist=False parameter

    # Relationship to Playlist (one-to-many)
    playlists = db.relationship('Playlist', backref='user', lazy=True)

    # one to many relationship with the song ratings
    song_ratings = db.relationship('SongRating', backref='user', lazy=True)

class Artist(db.Model):
    __tablename__ = 'artist' 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # foreign key for one to one with user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    
    # one to many relationship with songs
    songs = db.relationship('Song', backref='artist', lazy=True) 

    # one to many relationship with albums
    albums = db.relationship('Album', backref='artist', lazy=True)

# many to many relationship b/w songs and playlists
playlist_songs = db.Table('playlist_songs',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
)

class Playlist(db.Model):
    __tablename__ = 'playlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    
    # foreign key of the user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # (many-to-many relationship for playlist-songs, omitted for brevity)
    songs = db.relationship('Song', secondary=playlist_songs, lazy='subquery', backref=db.backref('playlists', lazy=True))


class Song(db.Model):
    __tablename__= 'song'
    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    lyrics = db.Column(db.Text())
    
    # foreign key of the artist table
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=True)

    # foreign key of the album table
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=True)

    song_ratings = db.relationship('SongRating', backref='song', lazy=True, cascade='all, delete')
   

    def avg_song_rating(self):
        avg_rtng = db.session.query(db.func.avg(SongRating.rating)).filter(SongRating.song_id == self.id).scalar()
        return round(avg_rtng,2) if avg_rtng is not None else 'N/A'

# song rating table to store different ratings
class SongRating(db.Model):
    __tablename__ = 'song_rating'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating = db.Column(db.Float, nullable=False)

    # foreign key for the song table
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)

    # foreign key for the user table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


class Album(db.Model):
    __tablename__ = 'album'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False) 

    songs = db.relationship('Song', backref='album', lazy=True)



####################### Businelss Logic ########################


# separate admin signup
@app.route('/admin/signup', methods=['POST'])
def admin_signup():

    # check to make sure that only one admin is created
    if User.query.filter_by(role='admin').count() > 0:
       return jsonify({'message': 'An admin user already exists Another admin is not allowed'}), 400

    # getting the data from frontend api and storing it in variables
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    email = data.get('email')

    # querying the database to see if the user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Oops!! Username already exists'}), 400
    
    # creating an instance of user table
    user = User(name=name, email=email, username=username,password=generate_password_hash(password), role='admin')

    # adding the created user to the database
    db.session.add(user)

    # making final commit to the database
    db.session.commit()

    # finally returning response  to the fronend in json format
    return jsonify({'message': 'Admin Created successfully'}), 201

# user signup
@app.route('/signup', methods=['POST'])
def signup():

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    email = data.get('email')


    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Oops!! Username already exists.'}), 400

    user = User(name=name, email=email, username=username,password=generate_password_hash(password), role='user')
    # roie attribute is different in this case
    
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201



# artist signup
@app.route('/artist/signup', methods=['POST'])
def artist_signup():

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    email = data.get('email')


    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Oops!! Username already exists'}), 400

    # creating new user instance
    user = User(name=name, email=email, username=username,password=generate_password_hash(password), role='artist')
    
    # creating new artist instance
    new_artist = Artist()

    # connecting user and artist
    user.artist = new_artist

    # adding user to the database ( no need to add the artist separately it will be automatically added to the database)
    db.session.add(user)

    # making the commit
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # filtering the user from the database
    user = User.query.filter_by(username=username).first()

    # backend verification to see if user exists and password is correct
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    # access token creation 
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))

    # some extra information about the user
    user_info = {
        'user_id': user.id,
        'username': user.username,
        'name': user.name,
        'role': user.role,
        'email': user.email,
    }

    # sending access token and user data to the frontend in json format
    return jsonify({'access_token': access_token, 'user': user_info}), 200


@app.route('/api/logout', methods=['POST'])
@jwt_required()  
# it enforces that this end-point will only be accessed if there is a valid token attached with the request
# otherwise it will throw 401 (unauthorized) error
def logout():
    response = jsonify({'message':'Logged out successfully'})

    # removing all the tokens from the backend
    unset_jwt_cookies(response)
    return response, 200


##################### Users Start ####################


@app.route('/users')
@jwt_required()
def get_users():
    user_id = get_jwt_identity() # identity of the access token recieved from the frontend

    # getting the user info from the database
    user = User.query.filter_by(id=user_id).first()

    # checking if the user is of admin type, if not throwing an error
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized You are not an admin'}), 401

    # getting all users from the database
    all_users = User.query.filter_by(role='user').all()

    # making the users list json friendly
    user_list = [
        {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'username': user.username,
            'role': user.role,
            'flagged': user.flagged
        }

        # for loop for all users ( each user object is a dictionary )
        for user in all_users
    ]

    # sending the user list back
    return jsonify(user_list), 200

@app.route('/flag/user/<int:user_id>', methods=['POST'])
@jwt_required()
def flag_user(user_id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized You are not an admin'}), 401

    
    user = User.query.filter_by(id=user_id).first()

    # updating the flagged attribute of the user
    user.flagged = True
    db.session.commit()
    return jsonify({'message': 'User flagged successfully'}), 200

@app.route('/unflag/user/<int:user_id>', methods=['POST'])
@jwt_required()
def unflag_user(user_id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized You are not an admin'}), 401

    user = User.query.filter_by(id=user_id).first()
    user.flagged = False
    db.session.commit()
    return jsonify({'message': 'User unflagged successfully'}), 200

@app.route('/delete/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized You are not an admin'}), 401

    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200


@app.route('/artists')
@jwt_required()
def get_artists():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized You are not an admin'}), 401
        
    artists = Artist.query.all()
    artist_list = [
        {
            'id': artist.id,
            'name': artist.user.name,
            'email': artist.user.email,
            'username': artist.user.username, # getting the username from user table from artist instance
            
         
        }

        for artist in artists
    ]
    return jsonify(artist_list), 200



##################### Users End ####################

############### Albums Start ####################

@app.route('/albums')
@jwt_required()
def get_albums(user_id=0):
    albums = []
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    # checking to see if the user is an artist
    if not user.artist:
        albums = Album.query.all()
    else:
        # if user is an artist filtering the albums of that artist only
        albums = Album.query.filter_by(artist_id=user.artist.id).all()

    album_list = [
        {
            'id': album.id,
            'title': album.title,
            'artist': album.artist.user.name,
            'songs': [(song.title, song.id) for song in album.songs]
        }

        for album in albums
    ]
    return jsonify(album_list), 200

@app.route('/album/create', methods=['POST'])
@jwt_required()
def create_album():
    
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user.role != 'artist':
        return jsonify({'message': 'Only artists can upload songs'}), 401

    # getting the title from the request using request.form.get ( request.get_json will also work )
    title = request.form.get('title')
    
    artist = Artist.query.filter_by(user_id=user_id).first()
    artist_id = artist.id

    new_album = Album(title=title, artist_id=artist_id)
    
    artist.albums.append(new_album)
    db.session.commit()
    return jsonify({'message': 'Album created successfully'}), 201

@app.route('/album/edit/<int:song_id>', methods=['PUT'])
@jwt_required()
def edit_album(album_id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user.role != 'artist':
        return jsonify({'message': 'Only artists can upload songs'}), 401
    
    album = Album.query.filter_by(id=album_id).first()
    title = request.form.get('title')
    # updating the title
    album.title = title

    db.session.commit()
    return jsonify({'message': 'Album Edited successfully'}), 200

@app.route('/album/add/song/<int:song_id>/<int:album_id>', methods=['POST'])
@jwt_required()
def add_song_to_album(song_id, album_id):

    song = Song.query.filter_by(id=song_id).first()
    album = Album.query.filter_by(id=album_id).first()

    if song in album.songs:
        return jsonify({'message': 'Song already exists in album'}), 400

    album.songs.append(song)
    db.session.commit()
    return jsonify({'message': 'Song added to album successfully'}), 200

@app.route('/album/remove/song/<int:songId>/<int:albumId>', methods=['POST','DELETE'])
@jwt_required()
def remove_song_from_album(songId, albumId):
    
    song = Song.query.filter_by(id=songId).first()
    album = Album.query.filter_by(id=albumId).first()

    album.songs.remove(song)
    db.session.commit()
    return jsonify({'message': 'Song removed from album successfully'}), 200



@app.route('/album/delete/<int:album_id>', methods=['DELETE'])
@jwt_required()
def delete_album(album_id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user.role != 'artist':
        return jsonify({'message': 'Only artists can upload songs'}), 401
    
    album = Album.query.filter_by(id=album_id).first()
    db.session.delete(album)
    db.session.commit()
    return jsonify({'message': 'Album deleted successfully'}), 200

############### Albums End ####################

################## Playlists Start ##################

@app.route('/playlist/create', methods=['POST'])
@jwt_required()
def create_playlist():

    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    name = request.form.get('name')
    description = request.form.get('description')

    new_playlist = Playlist(name= name, description=description)

    user.playlists.append(new_playlist)
    
    db.session.commit()
    return jsonify({'message': 'Playlist created successfully'}), 201

@app.route('/playlists')
@jwt_required()
def get_playlists():
    user_id = get_jwt_identity()
    playlists = Playlist.query.filter_by(user_id=user_id).all()
    playlist_list = [
        {
            'id': playlist.id,
            'name': playlist.name,
            'user': playlist.user.name,
            'songs': [(song.title, song.id) for song in playlist.songs],

            'description': playlist.description,
        }

        for playlist in playlists
    ]
    return jsonify(playlist_list), 200

@app.route('/playlist/delete/<int:playlist_id>', methods=['DELETE'])
@jwt_required()
def delete_playlist(playlist_id):
    playlist = Playlist.query.filter_by(id=playlist_id).first()
    db.session.delete(playlist)
    db.session.commit()
    return jsonify({'message': 'Playlist deleted successfully'}), 200

@app.route('/playlist/add/song/<int:songId>/<int:playlistId>', methods=['POST'])
@jwt_required()
def add_song_to_playlist(songId, playlistId):
    song = Song.query.filter_by(id=songId).first()
    playlist = Playlist.query.filter_by(id=playlistId).first()

    if song in playlist.songs:
        return jsonify({'message': 'Song already exists in playlist'}), 400

    playlist.songs.append(song)
    db.session.commit()
    return jsonify({'message': 'Song added to playlist successfully'}), 200

@app.route('/playlist/remove/song/<int:songId>/<int:playlistId>', methods=['POST','DELETE'])
@jwt_required()
def remove_song_from_playlist(songId, playlistId):
    

    song = Song.query.filter_by(id=songId).first()
    playlist = Playlist.query.filter_by(id=playlistId).first()

    playlist.songs.remove(song)
    db.session.commit()
    return jsonify({'message': 'Song removed from playlist successfully'}), 200

################## Playlists End ##################

################## Songs Start ##################


@app.route('/song/upload', methods=['POST'])
@jwt_required()
def upload_song():

    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    #verifying the token
    if not user:
        return jsonify({'message': 'Invalid Token'}), 401
        
    if user.role != 'artist':
        return jsonify({'message': 'Only artists can upload songs'}), 401

    title = request.form.get('title')
    lyrics = request.form.get('lyrics')

    artist = Artist.query.filter_by(user_id=user_id).first()
    artist_id = artist.id
    
    new_song = Song(title=title, lyrics=lyrics,  artist_id=artist_id)
   
    if artist:
        artist.songs.append(new_song)
    db.session.commit()
    
    return jsonify({'message': 'Song uploaded successfully'}), 201


@app.route('/songs')
@jwt_required()
def get_songs():
    songs = []
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    if not user.artist:
        songs = Song.query.all()
    else:
        songs = Song.query.filter_by(artist_id=user.artist.id).all()
    

    song_list = [
        {
            'id': song.id,
            'title': song.title,
            'lyrics': song.lyrics,
            'artist_name': song.artist.user.name,
            'artist_id': song.artist.id,
            'album': song.album.title if song.album else 'N/A',
            'showLyrics' : False,
            'avg_rating': song.avg_song_rating()
            
        }
        

        for song in songs
        
    ]
        
    return jsonify(song_list), 200
        

@app.route('/song/delete/<int:song_id>', methods=['GET','POST','DELETE'])
@jwt_required()
def delete_song(song_id):
    song = Song.query.filter_by(id=song_id).first()
    db.session.delete(song)
    db.session.commit()
    return jsonify({'message': 'Song deleted successfully'}), 200

@app.route('/song/edit/<int:song_id>', methods=['PUT'])
@jwt_required()
def edit_song(song_id):
    song = Song.query.filter_by(id=song_id).first()
    title = request.form.get('title')
    lyrics = request.form.get('lyrics')
    song.title = title
    song.lyrics = lyrics

    db.session.commit()
    return jsonify({'message': 'Song Edited successfully'}), 200




@app.route('/song/rate/<int:song_id>', methods=['POST'])
@jwt_required()
def rate_song(song_id):
    data = request.get_json()
    rating = data.get('rating')
    song_rating = SongRating(rating=rating, song_id=song_id)
    db.session.add(song_rating)
    db.session.commit()
    return jsonify({'message': 'Song rated successfully'}), 200

@app.route('/top/songs')
@jwt_required()
def top_songs():

    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized You are not an admin'}), 401
    
    songs = Song.query.all()
    songs = [song for song in songs if song.avg_song_rating() != 'N/A']
    songs.sort(key=lambda x: x.avg_song_rating(), reverse=True)
    song_list = [
        {
            'id': song.id,
            'title': song.title,
            'lyrics': song.lyrics,
            'artist_name': song.artist.user.name,
            'artist_id': song.artist.id,
            'album': song.album.title if song.album else 'N/A',
            'showLyrics' : False,
            'avg_rating': song.avg_song_rating()
            
        }

        for song in songs
    ]
    return jsonify(song_list), 200

################## Songs End ##################

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
