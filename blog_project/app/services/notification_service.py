# services/notification_service.py

from app.models.notification_model import Notification
from app import db

def create_notification(user_id, sender_id, type, post_id=None, comment_id=None):

    notification = Notification(
        user_id=user_id,       # who receives
        sender_id=sender_id,   # who performed action
        type=type,
        post_id=post_id,
        comment_id=comment_id
    )

    db.session.add(notification)
    db.session.commit()