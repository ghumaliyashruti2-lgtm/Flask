from app.models.like_model import Like
from app.models.post_model import Post
from app.extensions import db


def get_post_by_id(post_id):
    return Post.query.get(post_id)


def get_like(user_id, post_id):
    return Like.query.filter_by(
        user_id=user_id,
        post_id=post_id
    ).first()


def create_like(user_id, post_id):

    like = Like(
        user_id=user_id,
        post_id=post_id
    )

    db.session.add(like)
    db.session.commit()


def delete_like(like):

    db.session.delete(like)
    db.session.commit()