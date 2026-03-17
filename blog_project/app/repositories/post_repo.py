from app.models.post_model import Post
from app.extensions import db


#def get_all_posts():
    #return Post.query.order_by(Post.id.desc()).all()

def get_all_posts(page, per_page):
    return Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=per_page, error_out=False)

def get_post_by_id(post_id):
    return Post.query.get(post_id)


def save_post(post):
    db.session.add(post)
    db.session.commit()


def delete_post(post):
    db.session.delete(post)
    db.session.commit()


def update_post(post):
    db.session.commit()