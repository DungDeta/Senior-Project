import secrets
from flask import render_template, request, redirect, session
from flask_mail import Message
from src.app import app, bcrypt, redis_client, mail
from src.models.models import User
from src.services.user_services import add, check_duplicate, update
from src.utils.utils import generate_id, generate_verification_token, generate_expiration_timestamp

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    user = check_duplicate(request.form['username'], request.form['email'])
    if user is None:
        register_info = request.form
        if register_info['password'] == register_info['confirmPassword']:
            hashed_password = bcrypt.generate_password_hash(register_info.get('password')).decode('utf-8')
            token = generate_verification_token()
            user = User(generate_id(), register_info['username'], register_info['email'], hashed_password, token)
            add(user)

            token = secrets.token_urlsafe(16)
            user.token = token
            update(user)

            # Save OTP to Redis with a 5-minute expiration
            redis_client.setex(f"user:{user.id}", 300, user.___json__())  # 300 seconds = 5 minutes

            subject = 'Email Verification'
            body = render_template('verification_mail.html', token=token, userId=user.id,
                                   expires=generate_expiration_timestamp(24 * 60 * 60))
            sender = app.config['MAIL_DEFAULT_SENDER']
            recipients = [user.email]

            msg = Message(subject=subject, sender=sender, recipients=recipients)
            msg.html = body
            mail.send(msg)

            session['userId'] = user.___json__()
            return redirect('/mail/check_mailbox')

        return render_template('register.html', error_message='Password not match')

    return render_template('register.html', error_message='Username exists')