from src.app import db
from src.models.models import Advertisement

def add_advertisement(ad):
    db.session.add(ad)
    db.session.commit()

def update_advertisement(ad):
    db.session.commit()

def delete_advertisement(ad_id):
    ad = Advertisement.query.get(ad_id)
    db.session.delete(ad)
    db.session.commit()

def get_advertisements_paginate(page):
    return Advertisement.query.paginate(page=page, per_page=10)