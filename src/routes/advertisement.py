from flask import Blueprint, session, redirect, request, render_template
from datetime import datetime

from src.services.advertisement_services import (
    add_advertisement, update_advertisement, delete_advertisement,
    get_advertisements_paginate
)
from src.services.user_services import user_by_id
from src.utils.utils import convert_user_id_json_to_user_id, generate_id
from src.models.models import Advertisement

advertisement_blueprint = Blueprint('advertisement', __name__, template_folder='/templates',
                                    url_prefix='/advertisement')



@advertisement_blueprint.route('/add', methods=['POST'])
def add_ad():
    if session and 'userId' in session:
        user_id_json = session['userId']
        user_id = convert_user_id_json_to_user_id(user_id_json)
        user = user_by_id(user_id)

        if user.is_administrator:
            title = request.form.get('title')
            description = request.form.get('description')
            image = request.form.get('image')
            url = request.form.get('url')
            expiration_date = datetime.strptime(request.form.get('expiration_date'), '%Y-%m-%d')

            ad = Advertisement(
                generate_id(),
                title,
                description,
                image,
                url,
                expiration_date
            )

            add_advertisement(ad)

    return redirect('/advertisement_management/1')


@advertisement_blueprint.route('/update', methods=['POST'])
def update_ad():
    if session and 'userId' in session:
        user_id_json = session['userId']
        user_id = convert_user_id_json_to_user_id(user_id_json)
        user = user_by_id(user_id)

        if user.is_administrator:
            ad_id = request.form.get('id')
            ad = Advertisement.query.get(ad_id)

            if ad:
                ad.title = request.form.get('title')
                ad.description = request.form.get('description')
                ad.image = request.form.get('image')
                ad.url = request.form.get('url')
                ad.expiration_date = datetime.strptime(
                    request.form.get('expiration_date'),
                    '%Y-%m-%d'
                )

                update_advertisement(ad)

    return redirect('/advertisement_management/1')


@advertisement_blueprint.route('/delete', methods=['GET'])
def delete_ad():
    if session and 'userId' in session:
        user_id_json = session['userId']
        user_id = convert_user_id_json_to_user_id(user_id_json)
        user = user_by_id(user_id)

        if user.is_administrator:
            ad_id = request.args.get('id')
            delete_advertisement(ad_id)

    return redirect('/advertisement_management/1')