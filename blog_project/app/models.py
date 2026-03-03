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
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

    posts = db.relationship("Post", backref="author", lazy=True)
    # backref="author" means its connection between post and user bakcref is used for automatic reverse connection post->user and user->post access.
    
class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))