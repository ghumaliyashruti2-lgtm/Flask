from app.models.post_model import Post
from ..repositories.post_repo import (
    get_all_posts,
    get_post_by_id,
    save_post,
    delete_post,
    update_post
)

def get_posts_service():

    posts = get_all_posts()

    data = []

    for post in posts:
        data.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id
        })

    return {"posts": data}, 200

def create_post_service(data, user_id):

    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return {"error": "Title and content required"}, 400

    post = Post(
        title=title,
        content=content,
        user_id=user_id
    )

    save_post(post)

    return {
        "message": "Post created",
        "post_id": post.id
    }, 201
    
    
def delete_post_service(post_id, user_id):

    post = get_post_by_id(post_id)

    if not post:
        return {"error": "Post not found"}, 404

    if post.user_id != user_id:
        return {"error": "Not allowed"}, 403

    delete_post(post)

    return {"message": "Post deleted"}, 200

def edit_post_service(post_id, data, user_id):

    post = get_post_by_id(post_id)

    if not post:
        return {"error": "Post not found"}, 404

    if post.user_id != user_id:
        return {"error": "Not allowed"}, 403

    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)

    update_post(post)

    return {"message": "Post updated"}, 200