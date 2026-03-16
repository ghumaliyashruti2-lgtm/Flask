from ..repositories.search_repo import (
    search_posts,
    search_comments
)

def search_service(query):

    if not query:
        return {"error": "Search query required"}, 400

    posts = search_posts(query)
    comments = search_comments(query)

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
            "post_id": c.post_id,
            "user_id": c.user_id
        }
        for c in comments
    ]

    return {
        "posts": post_data,
        "comments": comment_data
    }, 200