from flask import Flask
# , request, redirect, url_for
from .routes import blueprint, app
from .database import init_app
from flask_session import Session

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.register_blueprint(blueprint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Initialize SQLAlchemy
init_app(app)

