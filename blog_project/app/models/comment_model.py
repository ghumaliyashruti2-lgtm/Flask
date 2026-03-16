from app.extensions import db

class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))    
    