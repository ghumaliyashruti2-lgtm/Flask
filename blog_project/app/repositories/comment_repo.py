from app.extensions import db
from app.models.comment_model import Comment


def save_comment(comment):
    db.session.add(comment)
    db.session.commit()
    
def get_all_comments():
    return Comment.query.all()


def get_comments_by_post(post_id):

    return Comment.query.filter_by(
        post_id=post_id,
    ).all()


def get_comment_by_id(comment_id):

    return Comment.query.get(comment_id)


def delete_comment(comment):

    db.session.delete(comment)
    db.session.commit()


def update_comment():
    db.session.commit()