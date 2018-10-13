from flask import Flask, Response, abort, request, jsonify, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required

from db import db
from login import login_manager
import models

app = Flask(__name__)
app.config.from_envvar('ROBIN_CONFIG')

db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def user_loader(user_id):
    return models.User.query.get(user_id)


@app.route('/')
def home():
    if current_user.is_authenticated:
        return 'Hello, %s.' % current_user.name

    return 'Hello, world!'


@app.route('/auth/login', methods=['GET', 'POST'])
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


@app.route('/auth/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/auth/register', methods=['POST'])
def register():
    user = models.User(
        name=request.form.get('name'),
        email=request.form.get('email'),
        password=request.form.get('password'),
    )
    db.session.add(user)
    db.session.commit()

    return 'Added user.'


@app.route('/auth/_users')
def hidden_users():
    users = models.User.query.all()

    return jsonify(list(map(lambda user: {'id': user.id, 'email': user.email}, users)))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
