from flask import Flask
import psycopg2
from dotenv import load_dotenv
from config import Config
from flask_bcrypt import Bcrypt

load_dotenv()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Load configurations
    app.config.from_object(Config)
    print("Loaded POSTGRESQL_URI:", app.config['POSTGRESQL_URI'])
    print("Loaded SECRET_KEY:", app.config['SECRET_KEY'])
    
    app.secret_key = app.config['SECRET_KEY']
    
    # Connect to PostgreSQL and print version
    conn = psycopg2.connect(app.config['POSTGRESQL_URI'])
    cur = conn.cursor()
    cur.execute('SELECT VERSION()')
    version = cur.fetchone()[0]
    print(f"Connected to PostgreSQL Database. Version: {version}")
    
    from .routes import routes  # Import the Blueprint
    app.register_blueprint(routes)  # Register the Blueprint

    return app  # Only return the app instance