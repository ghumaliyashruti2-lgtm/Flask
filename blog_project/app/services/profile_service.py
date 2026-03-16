from ..repositories.profile_repo import (
    get_user_by_username,
    get_user_posts,
    get_user_comments,
    get_user_likes,
    update_user
)

from ..utils.file_upload import (
    allowed_file,
    save_profile_picture,
    delete_profile_picture
)

from app.models.user_model import User

def get_user_profile_service(username):

    user = get_user_by_username(username)

    if not user:
        return {"error": "User not found"}, 404

    posts = get_user_posts(user.id)
    comments = get_user_comments(user.id)
    likes = get_user_likes(user.id)

    post_data = [
        {
            "id": p.id,
            "title": p.title,
            "content": p.content
        }
        for p in posts
    ]

    comment_data = [
        {
            "id": c.id,
            "text": c.text,
            "post_id": c.post_id
        }
        for c in comments
    ]

    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "profile_pic": user.profile_pic
        },
        "posts": post_data,
        "comments": comment_data,
        "likes_count": len(likes)
    }, 200
    
    
def upload_profile_picture_service(file, user_id):
    
    user = User.query.get(user_id)
    
    if not file:
        return {"error": "No file uploaded"}, 400

    if not allowed_file(file.filename):
        return {"error": "Invalid file type"}, 400

    filename = save_profile_picture(file)

    user.profile_pic = filename

    update_user()

    return {
        "message": "Profile picture updated",
        "filename": filename
    }, 200
    
    
def delete_profile_picture_service(user_id):
    
    user = user = User.query.get(user_id)

    if user.profile_pic != "default_profile.png":

        delete_profile_picture(user.profile_pic)

        user.profile_pic = "default_profile.png"

        update_user()

    return {"message": "Profile image removed"}, 200