
class Config:
    SECRET_KEY = "secret123"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SECRET_KEY = "secret"

    SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    MAIL_USERNAME = "ghumaliyashruti2@gmail.com"
    MAIL_DEFAULT_SENDER = "mini_blog@gmail.com"
    MAIL_PASSWORD ="wxtx wbvm ygri ffei"
    
    UPLOAD_FOLDER = "static/images/post_images"
    
    JWT_SECRET_KEY = "super-secret-key"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access"]
    from datetime import timedelta
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)