import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

class Config:
    POSTGRESQL_URI = os.getenv('POSTGRESQL_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')