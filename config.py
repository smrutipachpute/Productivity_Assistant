import os

# Define the base directory
BASE_DIR = os.path.abspath(os.path.dirname(__name__))

# Configuration options
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SECRET_KEY = 'your_secret_key'