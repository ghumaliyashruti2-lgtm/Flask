from flask import Blueprint, request,  jsonify
from .models import Comment
from . import db
from flask_login import  login_required
from flask_login import current_user

comment_api = Blueprint("comment_api", __name__)


# ======================
# SHOW COMMENTS
# ======================

@comment_api.route("/comments/<int:post_id>", methods=["GET"])
@login_required
def show_comments_api(post_id):

    comments = Comment.query.filter_by(post_id=post_id).all()

    comment_list = []

    for comment in comments:

        # check if logged-in user wrote the comment
        if comment.user_id == current_user.id:
            username = "You"
        else:
            username = comment.author.username   # relationship user

        comment_list.append({
            "id": comment.id,
            "text": comment.text,
            "user": username,
            "post_id": comment.post_id
        })

    return jsonify(comment_list)

# ======================
# ADD COMMENT 
# =======================

@comment_api.route("/comment/<int:post_id>", methods=["POST"])
@login_required
def add_comment_api(post_id):

    data = request.get_json()

    text = data.get("comment")
    
    if not text:
        return jsonify({"error":"Comment cannot be empty"}),400

    comment = Comment(
        text=text,
        user_id=current_user.id,
        post_id=post_id
    )

    db.session.add(comment)
    db.session.commit()

    return jsonify({
        "message": "Comment added",
        "comment_id": comment.id
    })


# ==========================
# EDIT COMMENT
# =========================

@comment_api.route("/edit-comment/<int:id>", methods=["PUT"])
@login_required
def edit_comment_api(id):

    comment = Comment.query.get_or_404(id)

    if comment.user_id != current_user.id:
        return jsonify({"error": "Not allowed"}), 403

    data = request.get_json()

    content = data.get("content")

    if not content:
        return jsonify({"error": "Content cannot be empty"}), 400

    comment.text = content

    db.session.commit()

    return jsonify({
        "message": "Comment updated successfully",
        "comment_id": comment.id,
        "text": comment.text
    })
    
# =====================
# DELETE COMMENT 
# =====================

@comment_api.route("/delete-comment/<int:id>", methods=["DELETE"])
@login_required
def delete_comment_api(id):

    comment = Comment.query.get_or_404(id)

    if comment.author != current_user:
        return jsonify({"error": "Not allowed"}), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({
        "message": "Comment deleted"
    })

    
    