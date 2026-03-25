from app.extensions import db

class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    target_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))    
    
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)

    replies = db.relationship(
        'Comment',
        backref=db.backref('parent', remote_side=[id]),
        lazy=True
    )

    # ✅ CLEAN RELATIONSHIPS
    sender = db.relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="sent_comments"
    )

    receiver = db.relationship(
        "User",
        foreign_keys=[target_user_id],
        back_populates="received_comments"
    )