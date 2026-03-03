from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

login_manager = LoginManager()

db =  SQLAlchemy()

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    
    from .routes import main
    app.register_blueprint(main)

def create_app():

    from .models import User
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    
    login_manager.init_app(app)
    login_manager.login_view = "main.login"
    # here login_manager variable check if user login  then 
    # open file other wise redirect login page (function) in main blueprint

    @login_manager.user_loader # this is use a load a users .
    def load_user(user_id): # this a receive user id
        return User.query.get(int(user_id)) # fetch user where id is user id and return thata data.

    from .routes import main
    app.register_blueprint(main)

    return app
    