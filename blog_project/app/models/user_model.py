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

    posts = db.relationship("Post", backref="author", cascade="all, delete")
    likes = db.relationship("Like", backref="author", cascade="all, delete")

    # 🔔 Notifications
    received_notifications = db.relationship(
        "Notification",
        foreign_keys="Notification.user_id",
        back_populates="receiver",
        cascade="all, delete"
    )

    sent_notifications = db.relationship(
        "Notification",
        foreign_keys="Notification.sender_id",
        back_populates="sender",
        cascade="all, delete"
    )

    # ✅ COMMENTS (FIXED CLEAN)
    sent_comments = db.relationship(
        "Comment",
        foreign_keys="Comment.user_id",
        back_populates="sender",
        cascade="all, delete"
    )

    received_comments = db.relationship(
        "Comment",
        foreign_keys="Comment.target_user_id",
        back_populates="receiver",
        cascade="all, delete"
    )