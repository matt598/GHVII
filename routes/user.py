from flask import Blueprint, Response, abort, jsonify, redirect, request, url_for
from flask_login import login_required, login_user, logout_user

import models
from db import db

user_app = Blueprint('login', __name__, url_prefix='/auth')


@user_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = models.User.query.filter_by(email=email).first()
        print(user)
        if not user:
            return abort(401)

        if not user.check_password(password):
            return abort(401)

        login_user(user)

        return redirect(url_for('home'))
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=email>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')


@user_app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@user_app.route('/register', methods=['POST'])
def register():
    user = models.User(
        name=request.form.get('name'),
        email=request.form.get('email'),
        password=request.form.get('password'),
    )
    db.session.add(user)
    db.session.commit()

    return 'Added user.'


@user_app.route('/_users')
def hidden_users():
    users = models.User.query.all()

    return jsonify(list(map(lambda user: {'id': user.id, 'email': user.email}, users)))
