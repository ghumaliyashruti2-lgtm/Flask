from app.models.comment_model import Comment
from app.models.post_model import Post
from app.repositories.comment_repo import (
    save_comment,
    get_comments_by_post,
    get_comment_by_id,
    delete_comment,
    update_comment,
    get_all_comments
)

# ✅ ADD COMMENT (POST ID FROM URL)
def add_comment(post_id, data, user_id):

    text = data.get("text")

    if not text:
        return {"error": "Comment cannot be empty"}, 400

    # ✅ check post exists
    post = Post.query.get(post_id)
    if not post:
        return {"error": "Post not found"}, 404

    comment = Comment(
        text=text,
        user_id=user_id,
        post_id=post_id
    )

    save_comment(comment)

    return {"message": "Comment added"}, 201



def reply_comment(post_id, data, user_id):

    text = data.get("text")
    parent_id = data.get("parent_id")

    if not text:
        return {"error": "Reply cannot be empty"}, 400

    if not parent_id:
        return {"error": "parent_id required"}, 400

    comment = Comment(
        text=text,
        user_id=user_id,
        post_id=post_id,
        parent_id=parent_id
    )

    save_comment(comment)

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