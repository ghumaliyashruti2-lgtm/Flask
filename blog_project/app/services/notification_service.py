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
    
    
def delete_notification(notification_id, user_id):
    notification = Notification.query.get(notification_id)

    if not notification:
        return {"msg": "Notification not found"}, 404

    if notification.user_id != int(user_id):
        return {"msg": "Unauthorized"}, 403

    db.session.delete(notification)
    db.session.commit()

    return {"msg": "Notification deleted"}, 200