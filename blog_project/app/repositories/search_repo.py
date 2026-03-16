from app.models.post_model import Post
from app.models.comment_model import Comment
from sqlalchemy import or_


def search_posts(query):

    return Post.query.filter(
        or_(
            Post.title.ilike(f"%{query}%"),
            Post.content.ilike(f"%{query}%")
        )
    ).all()


def search_comments(query):

    return Comment.query.filter(
        Comment.text.ilike(f"%{query}%")
    ).all()