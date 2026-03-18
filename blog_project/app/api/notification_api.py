# routes/notification_api.py

from app import db
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.notification_model import Notification

notification_api = Blueprint("notification_api", __name__)

@notification_api.route("/notifications", methods=["GET"])
@jwt_required()
def get_notifications():

    user_id = get_jwt_identity()

    notifications = Notification.query.filter_by(user_id=user_id)\
        .order_by(Notification.created_at.desc())\
        .all()

    result = []

    for n in notifications:

        sender_name = n.sender.username   # 🔥 MAGIC HERE

        if n.type == "comment":
            message = f"{sender_name} commented on your post"

        elif n.type == "reply":
            comment_text = n.comment.text if n.comment else ""
            message = f"{sender_name} replied to your comment \"{comment_text}\""

        elif n.type == "like":
            message = f"{sender_name} liked your post"

        else:
            message = "New notification"

        result.append({
            "id": n.id,
            "message": message,
            "is_read": n.is_read,
            "created_at": n.created_at
        })

    return jsonify(result)

@notification_api.route("/notifications/<int:id>/read", methods=["PUT"])
@jwt_required()
def mark_as_read(id):

    notification = Notification.query.get(id)

    if not notification:
        return {"msg": "Not found"}, 404

    notification.is_read = True
    db.session.commit()

    return {"msg": "Marked as read"}