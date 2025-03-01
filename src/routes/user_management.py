from flask import render_template, session, redirect, request
from flaskr.app import app
from flaskr.services.user_services import user_by_id, get_user_list_paginate, count_user, count_administrator, \
    count_blocked_user, search_list_paginate
from flaskr.utils.utils import convert_user_id_json_to_user_id


@app.route('/user_management/<int:page>', methods=['GET', 'POST'])
def user_management(page):
    if session and 'userId' in session:
        user_id_json = session['userId']
        user_id = convert_user_id_json_to_user_id(user_id_json)
        user = user_by_id(user_id)
        keyword = ''
        if request.method == 'POST':
            keyword = request.form.get('keyword')
            if keyword is not None:
                session['keyword'] = {'keyword': keyword}
            else:
                session.pop('keyword', None)
        if 'keyword' in session:
            keyword = session['keyword']['keyword']
            users = search_list_paginate(keyword, page)
        else:
            users = get_user_list_paginate(page)
        user_number = count_user()
        administrator_number = count_administrator()
        blocked_user_number = count_blocked_user()
        if user.is_administrator:
            return render_template('user_management.html', current_user=user, users=users, user_number=user_number,
                                   administrator_number=administrator_number, blocked_user_number=blocked_user_number,
                                   keyword=keyword)

    return redirect('/home/1')
