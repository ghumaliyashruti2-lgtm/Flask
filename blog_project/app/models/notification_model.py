from app.extensions import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    type = db.Column(db.String(50))
    
    post_id = db.Column(db.Integer, nullable=True)
    comment_id = db.Column(db.Integer, nullable=True)

    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ IMPORTANT
    receiver = db.relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="received_notifications"
    )

    sender = db.relationship(
        "User",
        foreign_keys=[sender_id],
        back_populates="sent_notifications"
    )
    
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("post.id"),   
        nullable=True
    )

    comment_id = db.Column(
        db.Integer,
        db.ForeignKey("comment.id"),  
        nullable=True
    )

    post = db.relationship(
        "Post",
        foreign_keys=[post_id]
    )

    comment = db.relationship(
        "Comment",
        foreign_keys=[comment_id]
    )