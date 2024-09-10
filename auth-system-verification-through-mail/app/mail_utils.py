from flask_mail import Message
from app.extensions import mail
from itsdangerous import URLSafeTimedSerializer
from flask import url_for
import os

def send_verification_email(user):
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    token = serializer.dumps(user.email, salt='email-confirmation-salt')
    confirm_url = url_for('main.verify_email', token=token, _external=True)

    print(f'Token: {token}')
    print(f'Confirm URL: {confirm_url}')

    msg = Message('Confirm Your Account', sender=os.getenv('MAIL_USERNAME'), recipients=[user.email])
    msg.body = f'Please click the link to verify your account: {confirm_url}'
    
    try:
        mail.send(msg)
        print('Email sent successfully.')
    except Exception as e:
        print(f'Error sending email: {e}')
