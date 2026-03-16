from app.models.comment_model import Comment
from app.repositories.comment_repo import (
    save_comment,
    get_comments_by_post,
    get_comment_by_id,
    delete_comment,
    update_comment
)

def add_comment(data, user_id):

    content = data.get("content")
    post_id = data.get("post_id")

    if not content:
        return {"error": "Comment cannot be empty"}, 400

    comment = Comment(
        content=content,
        user_id=user_id,
        post_id=post_id
    )

    save_comment(comment)

    return {"message": "Comment added"}, 201

def reply_comment(data, user_id):

    content = data.get("content")
    post_id = data.get("post_id")
    parent_id = data.get("parent_id")

    parent_comment = get_comment_by_id(parent_id)

    if not parent_comment:
        return {"error": "Parent comment not found"}, 404

    reply = Comment(
        content=content,
        user_id=user_id,
        post_id=post_id,
        parent_id=parent_id
    )

    save_comment(reply)

    return {"message": "Reply added"}, 201

def edit_comment(comment_id, data, user_id):

    comment = get_comment_by_id(comment_id)

    if not comment:
        return {"error": "Comment not found"}, 404

    if comment.user_id != user_id:
        return {"error": "Unauthorized"}, 403

    comment.content = data.get("content")

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
            "content": c.content,
            "user_id": c.user_id,
            "replies": [
                {
                    "id": r.id,
                    "content": r.content,
                    "user_id": r.user_id
                } for r in c.replies
            ]
        })

    return {"comments": result}, 200
