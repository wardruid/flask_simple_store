from flask import Blueprint, render_template, request, session, flash, redirect, url_for, current_app
from flask_mail import Message
from store import celery
from store.extensions import mail

email_bp = Blueprint('celery_mail', __name__, template_folder='templates')


@email_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email

    # отправка почты
    json_msg = {
        "text": "Hello from Flask",
        "recipients": [request.form['email']],
        "body": "This is a test email sent from a background Celery task."
    }

    # msg = Message('Hello from Flask',
    #               recipients=[request.form['email']])
    # msg.body = 'This is a test email sent from a background Celery task.'
    if request.form['submit'] == 'Send':
        # send right away
        send_async_email.delay(json_msg)
        flash('Sending email to {0}'.format(email))
    else:
        # отправка почты через минуту
        send_async_email.apply_async(args=[json_msg], countdown=60)
        flash('An email will be sent to {0} in one minute'.format(email))

    return redirect(url_for('celery_mail.index'))


@celery.task
def send_async_email(json_msg):
    """Фоновое задание по отправке celery_mail с помощью Flask-Mail."""
    msg = Message(
        json_msg['text'],
        json_msg['recipients']
    )
    msg.body = json_msg['body']
    with current_app.app_context():
        mail.send(msg)
