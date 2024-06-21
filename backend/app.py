from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies

from datetime import timedelta, datetime

app = Flask(__name__)

#cors configuration
CORS(app, origins='*')

#database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mad2db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

#jwt configuration
app.config['JWT_SECRET_KEY'] = 'my-secret-key'
jwt = JWTManager(app)


### Models ###

class User(db.Model):
    __tablename__ = 'user' 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(1000))
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))

    role = db.Column(db.String())

### Business Logics (routes) ####

@app.route('/api/signup', methods=['POST'])
def signup():

    #getting the data from axios request
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    #checking if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Oops!! Username already exists.'}), 400

    #creating user instance 
    user = User(email=email, username=username,password=password, role='user')
    
    #adding the user to database
    db.session.add(user)

    # commiting the database
    db.session.commit()

    # returning json response to frontend
    return jsonify({'message': 'User registered successfully'}), 201



@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # filtering the user from the database
    user = User.query.filter_by(username=username).first()

    # checking to see if the password matches
    if not user and password != user.password:
        return jsonify({'message': 'Invalid Credentials'}), 401
    
    #creating access token
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(days = 1))
    
    # some extra information about the user
    user_info = {
        'user_id': user.id,
        'username': user.username,
        'role': user.role,
        'email': user.email,
    }

    return jsonify({'access_token':access_token, 'user':user_info}), 200

@app.route('/api/logout', methods=['POST'])
@jwt_required()  # it enforces that this end-point will only be accessed if there is a valid token attached with the request
def logout():
    response = jsonify({'message':'Logged out successfully'})

    # removing all the tokens from the backend
    unset_jwt_cookies(response)
    return response, 200


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)