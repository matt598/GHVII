from flask import Blueprint, abort, jsonify, redirect, request, url_for, render_template
from flask_login import login_user, logout_user

import models
from db import db

user_app = Blueprint('login', __name__, url_prefix='/auth')


@user_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email')
    password = request.form.get('password')

    user = models.User.query.filter_by(email=email).first()
    print(user)
    if not user:
        return abort(401)

    if not user.check_password(password):
        return abort(401)

    login_user(user)

    if user.person:
        return redirect(url_for('profile.view'))

    if user.service:
        return redirect(url_for('person.find'))

    return redirect(url_for('home'))


@user_app.route('/logout')
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
