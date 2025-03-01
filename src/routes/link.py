from flask import request, session, redirect, Blueprint, render_template

from src.app import bcrypt
from src.models.models import Link
from src.services.link_services import add, is_alias_exits, link_by_id, update, delete
from src.utils.utils import generate_alias, generate_id, convert_user_id_json_to_user_id

link_blueprint = Blueprint('links', __name__, template_folder='/templates', url_prefix='/links')


@link_blueprint.route('/shorten', methods=['POST'])
def shorten():
    link_info = request.form
    alias = link_info['alias']
    if alias is None or alias == '':
        alias = generate_alias(link_info['url'])
        while is_alias_exits(alias):
            alias = generate_alias(link_info['url'] + alias)

    id = generate_id()
    user_id_json = session['userId']
    user_id = convert_user_id_json_to_user_id(user_id_json)
    link = Link(id, alias, link_info['url'], user_id)
    add(link)
    previous_url = request.referrer
    if previous_url is None:
        return redirect('/home/1')

    return redirect(previous_url)


@link_blueprint.route('/update', methods=['POST'])
def update_link():
    link_info = request.form
    link = link_by_id(link_info['id'])
    link.alias = link_info['alias']
    link.url = link_info['url']
    if link is not None:
        update(link)

    previous_url = request.referrer
    if previous_url is None:
        return redirect('/home/1')

    return redirect(previous_url)


@link_blueprint.route('/delete', methods=['GET'])
def delete_link():
    id = request.args.get('id')
    link = link_by_id(id)
    if link is not None:
        delete(link)

    previous_url = request.referrer
    if previous_url is None:
        return redirect('/home/1')

    return redirect(previous_url)


@link_blueprint.route('/change_password', methods=['POST'])
def change_password():
    link_info = request.form
    link = link_by_id(link_info['id'])
    if link is not None:
        hashed_password = bcrypt.generate_password_hash(link_info.get('password')).decode('utf-8')
        link.password = hashed_password
        update(link)

    previous_url = request.referrer
    if previous_url is None:
        return redirect('/home/1')

    return redirect(previous_url)


@link_blueprint.route('/delete_password', methods=['GET'])
def delete_password():
    id = request.args.get('id')
    link = link_by_id(id)
    if link is not None:
        link.password = None
        update(link)

    previous_url = request.referrer
    if previous_url is None:
        return redirect('/home/1')

    return redirect(previous_url)


@link_blueprint.route('/mark_phishing', methods=['GET'])
def mark_phishing():
    id = request.args.get('id')
    link = link_by_id(id)
    if link is not None:
        if link.is_phishing:
            link.is_phishing = False
        else:
            link.is_phishing = True

        update(link)

    previous_url = request.referrer
    if previous_url is None:
        return redirect('/link_management/1')

    return redirect(previous_url)


@link_blueprint.route('/check_password', methods=['POST'])
def check_shorten_link_password():
    link = link_by_id(request.form.get('id'))
    password = request.form.get('password')
    if bcrypt.check_password_hash(link.password, password):
        return redirect(link.url)

    return render_template('redirect_shorten_link.html', link_id=link.id, error_message='Password is invalid')
