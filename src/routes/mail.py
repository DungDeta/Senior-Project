from flask import Blueprint, session, render_template, redirect, request

from src.app import redis_client
from src.services.user_services import user_by_id, update
from src.utils.utils import convert_user_id_json_to_user_id, get_current_timestamp

mail_blueprint = Blueprint('mail', __name__, template_folder='/templates', url_prefix='/mail')


@mail_blueprint.route('/check_mailbox', methods=['GET'])
def check_mailbox():
    if session and 'userId' in session:
        user_id_json = session['userId']
        user_id = convert_user_id_json_to_user_id(user_id_json)
        user = user_by_id(user_id)
        session.pop('userId', None)
        if not user.is_verified:
            return render_template('check_mailbox.html')

    return redirect('/')


@mail_blueprint.route('/verify/<string:user_id>', methods=['GET'])
def verify_mailbox(user_id):
    user = user_by_id(user_id)
    if user is not None and not user.is_verified:
        token = request.args.get('token')
        expires = int(request.args.get('expires'))

        redis_token = redis_client.get(f"user_token:{user_id}")  # Lấy token từ redis
        if redis_token == token and get_current_timestamp() < expires:
            user.is_verified = True
            update(user)
            session['userId'] = user.___json__()

    return redirect('/')
