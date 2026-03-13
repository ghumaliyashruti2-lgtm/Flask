from flask import Blueprint,  request, jsonify
from .models import Post , Like , Comment
from . import db
from flask_login import login_required
from flask_login import current_user
from sqlalchemy import or_

like_api = Blueprint("like_api", __name__)

# ==================
# LIKE / UNLIKE POST
# ==================
@like_api.route("/like/<int:post_id>", methods=["POST"])
@login_required
def like_post(post_id):

    post = Post.query.get_or_404(post_id)

    like = Like.query.filter_by(
        user_id=current_user.id,
        post_id=post_id
    ).first()

    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({"message": "Post unliked"})
    else:
        new_like = Like(
            user_id=current_user.id,
            post_id=post_id
        )
        db.session.add(new_like)
        db.session.commit()

        return jsonify({"message": "Post liked"})
    
# ====================
# SEARCH 
# ====================
@like_api.route("/search")
def search_api():

    query = request.args.get("query", "").strip()

    if not query:
        return jsonify({"error": "Search query required"}), 400

    # 🔎 search in posts
    posts = Post.query.filter(
        or_(
            Post.title.ilike(f"%{query}%"),
            Post.content.ilike(f"%{query}%")
        )
    ).all()

    # 🔎 search in comments
    comments = Comment.query.filter(
        Comment.text.ilike(f"%{query}%")
    ).all()

    post_data = []
    comment_data = []

    for post in posts:
        post_data.append({
            "id": post.id,
            "title": post.title,
            "content": post.content
        })

    for comment in comments:
        comment_data.append({
            "id": comment.id,
            "text": comment.text,
            "post_id": comment.post_id,
            "user_id": comment.user_id
        })

    return jsonify({
        "posts": post_data,
        "comments": comment_data
    })