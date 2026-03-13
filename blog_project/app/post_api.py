from flask import Blueprint, request, jsonify
from .models import Post 
from . import db
from flask_login import login_required
from flask_login import current_user

post_api = Blueprint("post_api", __name__)

   
# =======================
# GET POST IN PAGINATION 
# =======================

'''@post_api.route("/posts")
def get_posts():

    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.id.desc()).paginate(
        page=page,
        per_page=5
    )

    data = []

    for post in posts.items:
        data.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id
        })

    return jsonify({
        "posts": data,
        "page": page
    })'''
    
    
# =====================
# GET POST IN ONE PAGE 
# ==================== 


@post_api.route("/posts")
def get_posts():

    posts = Post.query.order_by(Post.id.desc()).all()

    data = []

    for post in posts:
        data.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id
        })

    return jsonify({
        "posts": data
    })  

# ==================
# ADD POST 
# ===================

@post_api.route("/posts", methods=["POST"])
@login_required
def create_post():

    data = request.get_json()

    title = data.get("title")
    content = data.get("content")
    
    if not title or not content:
        return jsonify({"error":"Title and content required"}),400

    post = Post(
        title=title,
        content=content,
        user_id=current_user.id
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({
        "message":"Post created",
        "post_id": post.id
    })
    

# ==================
# EDIT POST 
# ===================    


@post_api.route("/posts/<int:id>", methods=["PUT"])
@login_required
def edit_post_api(id):

    post = Post.query.get_or_404(id)

    if post.author != current_user:
        return jsonify({"error":"Not allowed"}),403

    data = request.get_json()

    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)

    db.session.commit()

    return jsonify({
        "message":"Post updated"
    })


# ==================
# DELET POST 
# ===================

@post_api.route("/posts/<int:id>", methods=["DELETE"])
@login_required
def delete_post_api(id):

    post = Post.query.get_or_404(id)

    if post.author != current_user:
        return jsonify({"error":"Not allowed"}),403

    db.session.delete(post)
    db.session.commit()

    return jsonify({
        "message":"Post deleted"
    })
