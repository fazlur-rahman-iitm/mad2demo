from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies

from datetime import timedelta, datetime

from flask_migrate import Migrate

from flask_caching import Cache

from worker import celery_init_app
from tasks import celery_test, celery_beat, monthly_report
from celery.result import AsyncResult

app = Flask(__name__)

celery_app = celery_init_app(app)

#cors configuration
CORS(app, origins='*')

#database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mad2db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# db migrate config
migrate = Migrate(app, db)

#jwt configuration
app.config['JWT_SECRET_KEY'] = 'my-secret-key'
jwt = JWTManager(app)





# Configuration for Flask-Caching
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'  # or the hostname of your Redis server
app.config['CACHE_REDIS_PORT'] = 6379         # or the port number of your Redis server
app.config['CACHE_REDIS_DB'] = 0              # the database number (0 by default)
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'  # alternative way to set Redis URL

# Initialize the cache
cache = Cache(app)


# mail configuration
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = '23f1001897@ds.study.iitm.ac.in'
app.config['MAIL_PASSWORD'] = 'fxxk uaap stft mgaz' # app password created in google not the gmail password
app.config['MAIL_DEFAULT_SENDER'] = '23f1001897@ds.study.iitm.ac.in'

mail = Mail(app)

# sedding a mail from flask-api
@app.route('/email/test')
def send_email():
  msg = Message(
    'Hello',
    recipients=['21f3000028@ds.study.iitm.ac.in','21f3001238@ds.study.iitm.ac.in'],
    body='This is a test email sent from Flask-Mail!'
  )
  # attach a pdf file 
  msg.attach('test.pdf', 'application/pdf', open('test.pdf', 'rb').read())

  # attach a string as a file
  msg.attach('hello.txt', 'text/plain', 'Hello, World!')

  mail.send(msg)
  return 'Email sent succesfully!'

# sending a mail using celery
@app.route('/celery/mail', methods  =['GET', 'POST'])
def celery_mail():
    result = monthly_report.delay(['22f2000931@ds.study.iitm.ac.in'])
    return jsonify({'task_id': str(result)})



@app.route('/cache')
@cache.cached(timeout=30)
def index():
    return  str(datetime.now())


    
# celery beat periodic task setup and execution
from celery.schedules import crontab

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    
    # Executes every 20 seconds
    sender.add_periodic_task(20.0, celery_beat.s(), name='add every 10', expires=100)

    # Executes tasks every day at 6:16 (UTC).
    sender.add_periodic_task(
        crontab(minute=16, hour=6),
        celery_beat.s(),
    )
    # make sure the time is in UTC

class User(db.Model):
    __tablename__ = 'user' 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(1000))
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))

    role = db.Column(db.String())




@app.route('/api/celery/test', methods=['POST'])
def celery_test_endpoint():
    result = celery_test.delay(5,6)

    return jsonify({'task_id': str(result)})

@app.route('/api/celery/status/<task_id>', methods=['GET', 'POST'])
def celery_status_endpoint(task_id):
    result = AsyncResult(task_id)
    return jsonify({'status': result.state, 'result': result.result})

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

@app.route('/api/users', methods=['GET'])
@cache.cached(timeout=300)
@jwt_required()
def search_users():
    id = get_jwt_identity()
    current_user = User.query.get(id)
    print(current_user)
    users = User.query.all()
  
    search_query = request.args.get('search', '').lower()

    filtered_users = []
    for user in users:
        user_data = {
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'role' : user.role,
            'id' : user.id
        }
        if search_query in user.name.lower():
            filtered_users.append(user_data)

    if not filtered_users:
        return jsonify({'message': 'No users found'}), 200
    
    return jsonify(filtered_users)




with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)