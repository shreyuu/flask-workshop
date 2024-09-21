import psycopg2
from flask import current_app
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()

def get_last_user_id(postgresql_uri):
    with psycopg2.connect(postgresql_uri) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")
            last_user = cur.fetchone()
    
    return last_user[0] if last_user else None

def save_to_db(user_data):
    with psycopg2.connect(current_app.config['POSTGRESQL_URI']) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (name, id, gender, branch, phone, email, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_data['name'], user_data['ID'], user_data['gender'], user_data['branch'], user_data['phone'], user_data['email'], user_data['password']))
            conn.commit()

def verify_user(email, password):
    conn = psycopg2.connect(current_app.config['POSTGRESQL_URI'])
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    print("User fetched from database:", user)  # Debugging
    
    if user:
        if bcrypt.check_password_hash(user[-1], password):
            return {
                'ID': user[0],  # Change to the correct index for user ID
                'name': user[1],
                'gender': user[2],
                'branch': user[3],
                'phone': user[4],
                'email': user[5],
                # 'password': user[6]  # Avoid returning the password
            }
    
    return None