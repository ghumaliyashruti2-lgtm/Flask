from app.extensions import db
from datetime import datetime

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    image = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    comments = db.relationship("Comment", backref="post", cascade="all, delete")
    likes = db.relationship("Like", backref="post", cascade="all, delete")
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    