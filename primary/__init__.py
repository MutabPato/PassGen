from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Ininitialize SQLAlchemy to use in our models

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '8cadbb76-55a8-41c5-b94d-f68ebd11c66d'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    with app.app_context():
        from . import models # Load models first
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # user_id is just the primary key of our user table, we use it in the query for the user
        return User.query.get(int(user_id))

    # Blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app



