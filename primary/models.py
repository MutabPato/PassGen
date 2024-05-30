from flask_login import UserMixin
from . import db


# User model represents what it means for the app to have a user
# Models created in Flask-SQLAlchemy are represented by classes that then translate to tables in database

class User(UserMixin, db.Model):
    # UserMixin adds Flask-Login attributes to the model so that Flask-Login will be able to work with it
    # User with columns for an id, email, password and name
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))



