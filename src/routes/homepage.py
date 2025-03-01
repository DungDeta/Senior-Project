from flask import render_template, session, redirect, request
from flaskr.app import app
from flaskr.services.link_services import count_short_link_per_user, get_links_per_user_paginate, \
    search_list_per_user_paginate
from flaskr.services.user_services import user_by_id
from flaskr.utils.utils import convert_user_id_json_to_user_id


@app.route('/home/<int:page>', methods=['GET', 'POST'])
def homepage(page):
    if session and 'userId' in session:
        user_id_json = session['userId']
        user_id = convert_user_id_json_to_user_id(user_id_json)
        user = user_by_id(user_id)
        if not user.is_verified:
            return redirect('/mail/check_mailbox')
        keyword = ''
        if request.method == 'POST':
            keyword = request.form.get('keyword')
            if keyword is not None:
                session['keyword'] = {'keyword': keyword}
            else:
                session.pop('keyword', None)
        if 'keyword' in session:
            keyword = session['keyword']['keyword']
            links = search_list_per_user_paginate(keyword, page, user)
        else:
            links = get_links_per_user_paginate(user, page)
        short_link_number = count_short_link_per_user(user)
        total_click_times = 0
        for link in user.links:
            total_click_times += link.click_times

        return render_template('home.html', links=links, user=user, short_link_number=short_link_number,
                               total_click_times=total_click_times, keyword=keyword)

    return redirect('/')
