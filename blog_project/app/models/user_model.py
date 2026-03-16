from app.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(150), unique=True, nullable=False)

    email = db.Column(db.String(200), unique=True, nullable=False)

    password = db.Column(db.String(150), nullable=False)

    otp = db.Column(db.String(6))

    is_verified = db.Column(db.Boolean, default=False)

    profile_pic = db.Column(db.String(200), default="default_profile.png")
    posts = db.relationship("Post", backref="author", lazy="select",cascade="all, delete")
    comments = db.relationship("Comment", backref="author", lazy="select",cascade="all, delete")
    likes = db.relationship("Like", backref="author", lazy="select",cascade="all, delete")
     # backref="author" means its connection between post and user bakcref is used for automatic reverse connection post->user and user->post access.
    