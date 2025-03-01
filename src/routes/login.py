from flask import render_template, request, redirect, session

from src.app import app
from src.services.user_services import authenticate


@app.route('/', methods=['GET', 'POST'])
@app.route('/login')
def login():
    if request.method == 'GET':
        if session and 'userId' in session:
            return redirect('/home/1')

        return render_template('login.html')

    user = authenticate(request.form['username'], request.form['password'])
    if user is None:
        return render_template('login.html', error_message='Username or password is invalid')
    elif user.is_blocked:
        return render_template('login.html', error_message='User blocked')

    session['userId'] = user.___json__()
    return redirect('/home/1')
