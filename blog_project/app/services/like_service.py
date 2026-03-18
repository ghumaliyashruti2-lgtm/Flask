from app.services.notification_service import create_notification

from ..repositories.like_repo import (
    get_post_by_id,
    get_like,
    create_like,
    delete_like
)

def toggle_like_service(post_id, user_id):

    post = get_post_by_id(post_id)

    if not post:
        return {"error": "Post not found"}, 404

    like = get_like(user_id, post_id)

    if like:

        delete_like(like)

        return {"message": "Post unliked"}, 200

    create_like(user_id, post_id)
    
    if post.user_id != user_id:   # prevent self-like notification
        create_notification(
            user_id=post.user_id,   # receiver (post owner)
            sender_id=user_id,      # who liked
            type="like",
            post_id=post_id
        )

    return {"message": "Post liked"}, 200

    

    