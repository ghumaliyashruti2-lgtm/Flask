from app import db
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
from app.services.notification_service import create_notification
from app.models.notification_model import Notification

# ✅ HELPER: BUILD NESTED TREE
def build_comment_tree(comments):

    comment_dict = {}
    tree = []

    for c in comments:
        comment_dict[c.id] = {
            "id": c.id,
            "comment": c.text,
            "user_id": c.user_id,
            "post_id": c.post_id,
            "parent_id": c.parent_id,
            "replies": []
        }

    for c in comment_dict.values():
        if c["parent_id"]:
            parent = comment_dict.get(c["parent_id"])
            if parent:
                parent["replies"].append(c)
        else:
            tree.append(c)

    return tree


# ✅ ADD COMMENT
def add_comment(post_id, data, user_id):

    text = data.get("text")

    if not text:
        return {"error": "Comment cannot be empty"}, 400

    post = Post.query.get(post_id)
    if not post:
        return {"error": "Post not found"}, 404

    comment = Comment(
        text=text,
        user_id=user_id,
        post_id=post_id,
        parent_id=None
    )

    save_comment(comment)
    if post.user_id != user_id:
        create_notification(
            user_id=post.user_id,   # User2 (Diya) → receiver
            sender_id=user_id,      # User1 (Vidhi) → sender
            type="comment",
            post_id=post_id,
            comment_id=comment.id
        )

    return {"message": "Comment added"}, 201


# ✅ REPLY COMMENT
def reply_comment(post_id, data, user_id):

    text = data.get("text")
    parent_id = data.get("parent_id")

    if not text or not parent_id:
        return {"error": "Text and parent_id required"}, 400

    parent = get_comment_by_id(parent_id)

    if not parent:
        return {"error": "Parent comment not found"}, 404

    comment = Comment(
        text=text,
        user_id=user_id,
        post_id=post_id,
        parent_id=parent_id
    )

    save_comment(comment)
    
    if parent.user_id != user_id:
        create_notification(
            user_id=parent.user_id,   # 👈 Vidhi (comment owner)
            sender_id=user_id,        # 👈 Shruti (replier)
            type="reply",
            post_id=post_id,
            comment_id=comment.id    # ✅ USE NEW COMMENT (IMPORTANT)
        )

    return {"message": "Reply added"}, 201


# ✅ EDIT COMMENT
def edit_comment(comment_id, data, user_id):

    comment = get_comment_by_id(comment_id)

    if not comment:
        return {"error": "Comment not found"}, 404

    if comment.user_id != user_id:
        return {"error": "Unauthorized"}, 403

    text = data.get("text")
    if not text:
        return {"error": "Text required"}, 400

    comment.text = text

    update_comment(comment)   # ✅ FIXED

    return {"message": "Comment updated"}, 200


# ✅ DELETE COMMENT (WITH REPLIES 🔥)
def delete_with_replies(comment):

    for reply in comment.replies:
        delete_with_replies(reply)

    delete_comment(comment)


from app.models.notification_model import Notification

def remove_comment(comment_id, user_id):

    comment = Comment.query.get(comment_id)

    if not comment:
        return {"msg": "Comment not found"}, 404

    if comment.user_id != user_id:
        return {"msg": "Unauthorized"}, 403

    # 🔥 DELETE RELATED NOTIFICATIONS
    Notification.query.filter_by(comment_id=comment_id).delete()

    db.session.delete(comment)
    db.session.commit()

    return {"msg": "Comment deleted"}, 200


# ✅ GET COMMENTS (NESTED ✅)
def get_post_comments(post_id, page, per_page):

    pagination = get_comments_by_post(post_id, page, per_page)

    comments = pagination.items

    nested_comments = build_comment_tree(comments)

    return {
        "comments": nested_comments,
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page
    }, 200


# ✅ GET ALL COMMENTS
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