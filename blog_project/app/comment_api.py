from flask import Blueprint, request,  jsonify
from .models import Comment
from . import db
from flask_login import  login_required
from flask_login import current_user


comment_api = Blueprint("comment_api", __name__)

   
# ======================
# ADD AND SHOW COMMENT  
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

# ==========================
# EDIT COMMENT
# =========================

@comment_api.route("/edit-comment/<int:id>", methods=["PUT"])
@login_required
def edit_comment_api(id):

    comment = Comment.query.get_or_404(id)

    if comment.author != current_user:
        return jsonify({"error": "Not allowed"}), 403

    data = request.get_json()

    comment.text = data.get("text")

    db.session.commit()

    return jsonify({
        "message": "Comment updated"
    })




    
    