from operator import or_
from src.app import db, bcrypt
from src.models.models import User


def add(user):
    db.session.add(user)
    db.session.commit()


def update(user):
    user.verified = True
    db.session.commit()


def delete(user):
    db.session.delete(user)
    db.session.commit()


def user_by_id(id):
    return User.query.filter(User.id == id).one_or_none()


def get_user_list_paginate(page):
    return User.query.paginate(page=page, per_page=10)


def count_administrator():
    return User.query.filter(User.is_administrator == True).count()


def count_user():
    return User.query.count()


def count_blocked_user():
    return User.query.filter(User.is_blocked == True).count()


def search_list_paginate(keyword, page):
    return User.query.filter(
        or_(User.username.like("%" + keyword + "%"), User.email.like("%" + keyword + "%"))).paginate(page=page,
                                                                                                     per_page=10)


def check_duplicate(username, email):
    user = User.query.filter(or_(User.username == username, User.email == email)).one_or_none()
    return user


def authenticate(username, password):
    user = User.query.filter(or_(User.username == username, User.email == username)).one_or_none()
    if user is not None:
        if bcrypt.check_password_hash(user.password, password):
            return user
    return None
