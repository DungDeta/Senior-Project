from flask import render_template, session, redirect, request

from src.app import app
from src.services.advertisement_services import get_advertisements_paginate
from src.services.user_services import user_by_id
from src.utils.utils import convert_user_id_json_to_user_id


@app.route('/advertisement_management/<int:page>', methods=['GET', 'POST'])
def advertisement_management(page):
    if session and 'userId' in session:
        user_id_json = session['userId']
        user_id = convert_user_id_json_to_user_id(user_id_json)
        user = user_by_id(user_id)

        if user.is_administrator:
            advertisements = get_advertisements_paginate(page)
            return render_template('advertisement_management.html', user=user, advertisements=advertisements)

    return redirect('/home/1')