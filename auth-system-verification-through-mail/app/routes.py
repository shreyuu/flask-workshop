from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, User, bcrypt
from app.mail_utils import send_verification_email, send_account_verified_email
from itsdangerous import URLSafeTimedSerializer
import os
from datetime import datetime, timedelta
from flask_login import login_user
from app.extensions import mail
from flask_mail import Message
from authlib.integrations.flask_client import OAuth

main_routes = Blueprint('main', __name__)
oauth = OAuth()
google = oauth.register(
    'google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://127.0.0.1:5000/oauth2callback',
    client_kwargs={'scope': 'openid profile email'},
)

@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        # Check if a user with the same email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already registered. Please use a different one or log in.', 'danger')
            return redirect(url_for('main.register'))  
        
        # If email is unique, proceed to register the user
        user = User(username=username, email=email, password=password, is_active=False)  # Add is_active=False here
        db.session.add(user)
        db.session.commit()

        send_verification_email(user)
        flash('A verification email has been sent to your email address.', 'info')
        return redirect(url_for('main.login'))

    return render_template('html/register.html')

@main_routes.route('/verify/<token>')
def verify_email(token):
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    try:
        email = serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
        user = User.query.filter_by(email=email).first_or_404()
        user.is_active = True
        db.session.commit()
        
        # Send account verification email
        send_account_verified_email(user)

        flash('Your account has been verified!', 'success')
        login_user(user)
        return redirect(url_for('main.dashboard'))
    except Exception as e:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('main.register'))

@main_routes.route('/')
def home():
    return render_template('html/index.html')

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            if not user.is_active:
                flash('Please verify your email before logging in.', 'danger')
                return redirect(url_for('main.login'))
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.home')) 
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('html/login.html')


@main_routes.route('/verify-otp/<token>', methods=['GET', 'POST'])
def verify_otp(token):
    user = User.query.filter_by(email=token).first_or_404()

    if request.method == 'POST':
        entered_otp = request.form['otp']

        # Verify the OTP and check if it's within the allowed time limit (e.g., 1 hour)
        otp_age = datetime.utcnow() - user.otp_created_at
        if user.otp == entered_otp and otp_age < timedelta(hours=1):
            user.is_active = True
            db.session.commit()
            login_user(user)
            flash('Your account has been verified!', 'success')
            return redirect(url_for('main.login'))
        else:
            flash('Invalid or expired OTP.', 'danger')
            return redirect(url_for('main.verify_otp', token=token))

    return render_template('html/verify_otp.html', token=token)

#dubug
@main_routes.route('/test-email')
def test_email():
    msg = Message('Test Email', sender=os.getenv('MAIL_USERNAME'), recipients=['mshreyash.work@gmail.com'])
    msg.body = 'This is a test email.'
    try:
        mail.send(msg)
        return 'Test email sent!'
    except Exception as e:
        return f'Error sending email: {e}'

@main_routes.route('/login/google')
def login_google():
    redirect_uri = url_for('main.oauth_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@main_routes.route('/oauth2callback')
def oauth_callback():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    user_email = user_info.get('email')
    
    existing_user = User.query.filter_by(email=user_email).first()
    if existing_user:
        if not existing_user.is_active:
            flash('Please verify your email before logging in.', 'danger')
            return redirect(url_for('main.register'))

        flash('Logged in as: ' + user_email)
        login_user(existing_user)
    else:
        flash('User not found. Please register first.')
        return redirect(url_for('main.register'))
    
    return redirect(url_for('main.home'))