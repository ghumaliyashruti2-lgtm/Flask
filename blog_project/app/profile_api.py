from flask import Blueprint, request, jsonify
from .models import Post , Comment, Like
from . import db
from flask_login import login_required
from .models import User
from flask_login import current_user
import os
from flask import current_app
from werkzeug.utils import secure_filename

profile_api = Blueprint("profile_api", __name__)

# ====================
# PROFILE 
# ====================

# IMAGE EXTENTIONS  

ALLOWED_EXTENSIONS = {"png","jpg","jpeg","gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS


@profile_api.route("/user/<username>")
def user_profile_api(username):

    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(user_id=user.id).all()
    comments = Comment.query.filter_by(user_id=user.id).all()
    likes = Like.query.filter_by(user_id=user.id).all()

    post_data = []
    for post in posts:
        post_data.append({
            "id": post.id,
            "title": post.title,
            "content": post.content
        })

    comment_data = []
    for c in comments:
        comment_data.append({
            "id": c.id,
            "text": c.text,
            "post_id": c.post_id
        })

    return jsonify({
        "user": {
            "id": user.id,
            "username": user.username,
            "profile_pic": user.profile_pic
        },
        "posts": post_data,
        "comments": comment_data,
        "likes_count": len(likes)
    })
    
# ==========================
# UPLOAD PROFILE PICTURE 
# ==========================

@profile_api.route("/upload-profile-pic", methods=["POST"])
@login_required
def upload_profile_pic_api():

    file = request.files.get("profile_pic")
    
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error":"Invalid file type"}),400

    filename = secure_filename(file.filename)

    upload_folder = os.path.join(
        current_app.root_path,
        "static/images/profile_picture"
    )

    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, filename)

    file.save(filepath)

    current_user.profile_pic = filename
    db.session.commit()

    return jsonify({
        "message": "Profile picture updated",
        "filename": filename
    })
    
# =========================
# DELETE PROFILE IMAGE 
# =========================

@profile_api.route("/delete-profile-image", methods=["DELETE"])
@login_required
def delete_profile_image_api():

    if current_user.profile_pic != "default_profile.png":

        image_path = os.path.join(
            current_app.root_path,
            "static/images/profile_picture",
            current_user.profile_pic
        )

        if os.path.exists(image_path):
            os.remove(image_path)

        current_user.profile_pic = "default_profile.png"
        db.session.commit()

    return jsonify({
        "message": "Profile image removed"
    })
    