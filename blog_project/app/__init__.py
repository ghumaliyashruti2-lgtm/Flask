from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
db = SQLAlchemy()
mail = Mail()


def create_app():

    from .models import User

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "main.login"

    mail.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # HTML Routes
    from .routes import main
    app.register_blueprint(main)

    # API Routes
    from .auth_api import auth_api
    app.register_blueprint(auth_api, url_prefix="/api/auth")

    from .post_api import post_api
    app.register_blueprint(post_api, url_prefix="/api/post")

    from .comment_api import comment_api
    app.register_blueprint(comment_api, url_prefix="/api/comment")

    from .like_api import like_api
    app.register_blueprint(like_api, url_prefix="/api/like")

    from .profile_api import profile_api
    app.register_blueprint(profile_api, url_prefix="/api/profile")

    return app