# use SQLALchemy 
'''from . import db

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)'''
    
# used flask-login     

from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(150), unique=True, nullable=False)

    email = db.Column(db.String(200), unique=True, nullable=False)

    password = db.Column(db.String(150), nullable=False)

    otp = db.Column(db.String(6))

    is_verified = db.Column(db.Boolean, default=False)

    profile_pic = db.Column(db.String(200), default="default_profile.png")
    posts = db.relationship("Post", backref="author", lazy=True)
    comment = db.relationship("Comment", backref="author", lazy=True)
    likes = db.relationship("Like", backref="author", lazy=True)
     # backref="author" means its connection between post and user bakcref is used for automatic reverse connection post->user and user->post access.
    
class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    image = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    comments = db.relationship("Comment", backref="post", cascade="all, delete")
    likes = db.relationship("Like", backref="post", cascade="all, delete")
    
    
# comment 

class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))    
    
    
# like comment 

class Like(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))   
     