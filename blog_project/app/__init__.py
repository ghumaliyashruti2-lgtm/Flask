from flask import Flask
from .config import Config
from .extensions import db, login_manager, mail, jwt, jwt_blacklist
from .models.user_model import User


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "main.login"

    mail.init_app(app)
    jwt.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ⭐ JWT BLACKLIST CHECK (MUST BE INSIDE FUNCTION)
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in jwt_blacklist

    # API Routes
    from .api.auth_api import auth_api
    app.register_blueprint(auth_api, url_prefix="/api/auth")

    from .api.post_api import post_api
    app.register_blueprint(post_api, url_prefix="/api/post")

    from .api.comment_api import comment_api
    app.register_blueprint(comment_api, url_prefix="/api/comment")

    from .api.like_api import like_api
    app.register_blueprint(like_api, url_prefix="/api/like")

    from .api.search_api import search_api
    app.register_blueprint(search_api, url_prefix="/api/search")

    from .api.profile_api import profile_api
    app.register_blueprint(profile_api, url_prefix="/api/profile")

    return app