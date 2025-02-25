from operator import or_, and_

from sqlalchemy import func, distinct

from src.app import db
from src.models.models import Link


def add(link):
    db.session.add(link)
    db.session.commit()


def update(link):
    link.verified = True
    db.session.commit()


def delete(link):
    db.session.delete(link)
    db.session.commit()


def is_alias_exits(alias):
    link = Link.query.filter(Link.alias == alias).one_or_none()
    if link is None:
        return False

    return True


def link_by_id(id):
    return Link.query.filter(Link.id == id).one_or_none()


def link_by_alias(alias):
    return Link.query.filter(Link.alias == alias).one_or_none()


def get_link_list_paginate(page):
    return Link.query.paginate(page=page, per_page=10)


def count_short_link():
    return db.session.query(func.count(Link.alias)).scalar()


def count_short_link_per_user(user):
    return Link.query.filter(Link.user == user).count()


def count_url():
    return db.session.query(func.count(distinct(Link.url))).scalar()


def count_phishing_link():
    return Link.query.filter(Link.is_phishing == True).count()


def search_list_paginate(keyword, page):
    return Link.query.filter(or_(Link.url.like("%" + keyword + "%"), Link.alias.like("%" + keyword + "%"))).paginate(
        page=page, per_page=10)


def search_list_per_user_paginate(keyword, page, user):
    return Link.query.filter(and_((Link.user == user), or_(Link.url.like("%" + keyword + "%"),
                                                           Link.alias.like("%" + keyword + "%")))).paginate(
        page=page, per_page=10)


def get_links_per_user_paginate(user, page):
    return Link.query.filter(Link.user == user).paginate(page=page, per_page=10)
