from app.models.comment_model import Comment
from app.repositories.comment_repo import (
    save_comment,
    get_comments_by_post,
    get_comment_by_id,
    delete_comment,
    update_comment,
    get_all_comments
)

def add_comment(data, user_id):

    text = data.get("text")
    post_id = data.get("post_id")

    if not text:
        return {"error": "Comment cannot be empty"}, 400

    comment = Comment(
        text=text,
        user_id=user_id,
        post_id=post_id
    )

    save_comment(comment)

    return {"message": "Comment added"}, 201

def reply_comment(data, user_id):

    text = data.get("text")
    post_id = data.get("post_id")

    reply = Comment(
        text=text,
        user_id=user_id,
        post_id=post_id,
        
    )

    save_comment(reply)

    return {"message": "Reply added"}, 201

def edit_comment(comment_id, data, user_id):

    comment = get_comment_by_id(comment_id)

    if not comment:
        return {"error": "Comment not found"}, 404

    if comment.user_id != user_id:
        return {"error": "Unauthorized"}, 403

    comment.text = data.get("text")

    update_comment()

    return {"message": "Comment updated"}, 200


def remove_comment(comment_id, user_id):

    comment = get_comment_by_id(comment_id)

    if not comment:
        return {"error": "Comment not found"}, 404

    if comment.user_id != user_id:
        return {"error": "Unauthorized"}, 403

    delete_comment(comment)

    return {"message": "Comment deleted"}, 200

def get_post_comments(post_id):

    comments = get_comments_by_post(post_id)

    result = []

    for c in comments:
        result.append({
            "id": c.id,
            "text": c.text,
            "user_id": c.user_id,
            "post_id": c.post_id
        })

    return {"comments": result}, 200

def get_all_comments_service():

    comments = get_all_comments()

    result = []

    for c in comments:
        result.append({
            "id": c.id,
            "comment": c.text,
            "user_id": c.user_id,
            "post_id": c.post_id
        })

    return {"comments": result}, 200