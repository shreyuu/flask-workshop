from flask_mail import Message
from app.extensions import mail
from itsdangerous import URLSafeTimedSerializer
from flask import url_for
from datetime import datetime
import os
import random
from app import db

# Function to generate a 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Function to send verification email with OTP
def send_verification_email(user):
    otp = generate_otp()
    user.otp = otp
    user.otp_created_at = datetime.utcnow()

    db.session.commit()

    # Generate a confirmation link that directs to the OTP input page
    confirm_url = url_for('main.verify_otp', token=user.email, _external=True)

    msg = Message('Confirm Your Account with OTP', sender=os.getenv('MAIL_USERNAME'), recipients=[user.email])
    msg.body = f'Please click the link to verify your account and input your OTP: {confirm_url}.\nYour OTP is: {otp}'

    try:
        mail.send(msg)
        print('OTP and confirmation link sent successfully.')
    except Exception as e:
        print(f'Error sending OTP email: {e}')
        
        
def send_account_verified_email(user):
    print(f"Preparing to send verification email to {user.email}")
    msg = Message('Account Verified', sender=os.getenv('MAIL_USERNAME'), recipients=[user.email])
    verification_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg.body = f'Hello {user.username},\n\nYour account has been successfully verified on {verification_time}.\n\nThank you for registering!'
    
    try:
        mail.send(msg)
        print('Verification email sent successfully.')
    except Exception as e:
        print(f'Error sending email: {e}')