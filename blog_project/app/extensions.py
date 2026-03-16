from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_jwt_extended import JWTManager

login_manager = LoginManager()
db = SQLAlchemy()
mail = Mail()
jwt = JWTManager()
jwt_blacklist = set()