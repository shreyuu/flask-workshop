from flask import Blueprint, render_template, request, redirect, flash, current_app, session
import psycopg2
from app.models import save_to_db, get_last_user_id, verify_user
from flask_bcrypt import Bcrypt
from app.utils import generate_user_id

routes = Blueprint('routes', __name__)
bcrypt = Bcrypt()

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        branch = request.form['branch']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        last_user_id = get_last_user_id(current_app.config['POSTGRESQL_URI'])
        new_user_id = generate_user_id(last_user_id)
        
        user_data = {
            'name': name,
            'ID': new_user_id,
            'gender': gender,
            'branch': branch,
            'phone': phone,
            'email': email,
            'password': hashed_password
        }
        
        save_to_db(user_data)
        flash('Registration successful!', 'success')
        return redirect('/login')
    
    return render_template('register.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = verify_user(email, password)
        if user:
            session['user_id'] = user['ID']  # Store the user ID
            return redirect('/dashboard')
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@routes.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect('/login')
    
    user_id = session['user_id']
    print("User ID from session:", user_id)  # Check what user_id is in session

    # Fetch user information from the database
    conn = psycopg2.connect(current_app.config['POSTGRESQL_URI'])
    cur = conn.cursor()
    cur.execute("SELECT * FROM users_view WHERE id = %s", (user_id,))  # Make sure to query the right view
    user = cur.fetchone()
    print("User fetched from database:", user)  # Print the fetched user

    cur.close()
    conn.close()

    if user:
        user_info = {
            'ID': user[0],
            'name': user[1],
            'gender': user[2],
            'branch': user[3],
            'phone': user[4],
            'email': user[5],
        }
        return render_template('dashboard.html', user_info=user_info)
    
    flash('User not found.', 'danger')
    return redirect('/login')


@routes.route('/logout')
def logout():
    # Remove user_id from the session
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect('/login')