from app.models.user_model import User
from app.extensions import db


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def save_user(user):
    db.session.add(user)
    db.session.commit()


def update_user():
    db.session.commit()