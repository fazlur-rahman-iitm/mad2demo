from celery import shared_task
import time
from flask import Flask
app = Flask(__name__)
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = '23f1001897@ds.study.iitm.ac.in'
app.config['MAIL_PASSWORD'] = 'fxxk uaap stft mgaz' # app password created in google not the gmail password
app.config['MAIL_DEFAULT_SENDER'] = '23f1001897@ds.study.iitm.ac.in'

mail = Mail(app)


# celery test function
@shared_task(ignore_result=False)
def celery_test(x, y):
    print("celery test invoked")
    time.sleep(30)
    return x + y

# celery beat function
@shared_task(ignore_result=False)
def celery_beat():
    return "Hey! there!"

# sending a mail using celery
@shared_task(ignore_result=False)
def monthly_report(recipients):
    msg = Message(
    'Hello',
    recipients=recipients,
    body='This is a test email sent from Flask-Mail!'
  )

    mail.send(msg)
    return 'Email sent succesfully!'

