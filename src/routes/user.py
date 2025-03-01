from flask import Blueprint, session, redirect, request

from src.services.user_services import user_by_id, update, delete

user_blueprint = Blueprint('user', __name__, template_folder='/templates', url_prefix='/user')


@user_blueprint.route('/logout', methods=['POST'])
def logout():
    if session and 'userId' in session:
        session.pop('userId', None)

    return redirect('/')


@user_blueprint.route('/mark_administrator', methods=['GET'])
def mark_administrator():
    id = request.args.get('id')
    user = user_by_id(id)
    if user is not None:
        if user.is_administrator:
            user.is_administrator = False
        else:
            user.is_administrator = True

        update(user)

    return redirect("/user_management")


@user_blueprint.route('/block', methods=['GET'])
def block_user():
    id = request.args.get('id')
    user = user_by_id(id)
    if user is not None:
        if user.is_blocked:
            user.is_blocked = False
        else:
            user.is_blocked = True

        update(user)

    return redirect("/user_management")


@user_blueprint.route('/delete', methods=['GET'])
def delete_user():
    id = request.args.get('id')
    user = user_by_id(id)
    if user is not None:
        delete(user)

    previous_url = request.referrer
    if previous_url is None:
        return redirect('/home')

    return redirect(previous_url)


@user_blueprint.route('/update', methods=['POST'])
def update_user():
    user_info = request.form
    user = user_by_id(user_info['id'])
    user.username = user_info['username']
    user.email = user_info['email']
    update(user)

    previous_url = request.referrer
    if previous_url is None:
        return redirect('/home')

    return redirect(previous_url)
