from app.models.comment_model import Comment
from app.models.user_model import User
from app.models.post_model import Post
from app.models.like_model import Like
from app.extensions import db

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def get_user_posts(user_id):
    return Post.query.filter_by(user_id=user_id).all()


def get_user_comments(user_id):
    return Comment.query.filter_by(user_id=user_id).all()


def get_user_likes(user_id):
    return Like.query.filter_by(user_id=user_id).all()
    
def update_user(user):
    db.session.commit()