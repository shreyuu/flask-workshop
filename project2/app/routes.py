from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, User, bcrypt
from app.mail_utils import send_verification_email
from itsdangerous import URLSafeTimedSerializer
import os
from flask_login import login_user

main_routes = Blueprint('main', __name__)

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
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        send_verification_email(user)
        flash('A verification email has been sent to your email address.', 'info')
        return redirect(url_for('main.login'))

    return render_template('register.html')


@main_routes.route('/verify/<token>')
def verify_email(token):
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    try:
        email = serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
        user = User.query.filter_by(email=email).first_or_404()
        user.is_active = True
        db.session.commit()
        flash('Your account has been verified!', 'success')
        login_user(user)
        return redirect(url_for('main.dashboard'))
    except Exception as e:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('main.register'))
    
@main_routes.route('/')
def home():
    return render_template('index.html')

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))  # or any other page
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')