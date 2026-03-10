from flask import Blueprint,  request, jsonify
from .models import Post , Like
from . import db
from flask_login import login_required
from flask_login import current_user
from sqlalchemy import or_

like_api = Blueprint("like_api", __name__)

# ===========================
# LIKE POST 
# ==========================

@like_api.route("/like/<int:post_id>", methods=["POST"])
@login_required
def like_post_api(post_id):

    like = Like.query.filter_by(
        user_id=current_user.id,
        post_id=post_id
    ).first()

    if like:
        db.session.delete(like)
        action = "unliked"
    else:
        new_like = Like(
            user_id=current_user.id,
            post_id=post_id
        )
        db.session.add(new_like)
        action = "liked"

    db.session.commit()

    return jsonify({
        "message": action
    })

    
# ====================
# SEARCH 
# ====================

@like_api.route("/search")
def search_api():

    query = request.args.get("query","")

    if not query:
        return jsonify({"error":"Search query required"}),400
    
    posts = Post.query.filter(
        or_(
            Post.title.ilike(f"%{query}%"),
            Post.content.ilike(f"%{query}%")
        )
    ).all()

    data = []

    for post in posts:
        data.append({
            "id": post.id,
            "title": post.title,
            "content": post.content
        })

    return jsonify(data)