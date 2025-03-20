from flask import render_template, session, redirect, request
from sqlalchemy import or_
from flask import Blueprint, render_template, request, session, redirect
from src.app import app
from src.models.models import Link
from src.services.user_services import user_by_id
from src.utils.utils import convert_user_id_json_to_user_id

social_media_blueprint = Blueprint('social_media', __name__, template_folder='/templates', url_prefix='/social_media')
@social_media_blueprint.route('/<int:page>', methods=['GET', 'POST'])
def social_media(page):
    user = None
    if session and 'userId' in session:
        user_id_json = session['userId']
        user_id = convert_user_id_json_to_user_id(user_id_json)
        user = user_by_id(user_id)

    keyword = ''
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        if keyword is not None:
            session['social_keyword'] = {'keyword': keyword}
        else:
            session.pop('social_keyword', None)

    if 'social_keyword' in session:
        keyword = session['social_keyword']['keyword']
        links = Link.query.filter(
            Link.password.is_(None),  # Only links without password
            or_(Link.url.like("%" + keyword + "%"), Link.alias.like("%" + keyword + "%"))
        ).paginate(page=page, per_page=12)
    else:
        links = Link.query.filter(Link.password.is_(None)).paginate(page=page, per_page=12)

    return render_template('social_media.html', links=links, user=user, keyword=keyword)