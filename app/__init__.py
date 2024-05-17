from flask import Flask
# , request, redirect, url_for
from .routes import blueprint
from .database import init_app

app = Flask(__name__,template_folder='../templates', static_folder='../static')

app.register_blueprint(blueprint)

# Load configuration from config.py
# with open('./config.py', mode="rb"):
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# print("SQLALCHEMY_DATABASE_URI:", app.config['SQLALCHEMY_DATABASE_URI'])

# Initialize SQLAlchemy
init_app(app)

# Add more routes for task management, authentication, etc.
