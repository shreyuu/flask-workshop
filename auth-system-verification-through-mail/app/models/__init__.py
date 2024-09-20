from flask_login import UserMixin
from app.extensions import db, bcrypt
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    otp = db.Column(db.String(6), nullable=True) 
    otp_created_at = db.Column(db.DateTime, nullable=True) 

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"