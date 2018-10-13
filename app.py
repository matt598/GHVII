from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import current_user

from db import db
from login import login_manager
import models
import data

from routes.user import user_app
from routes.api import api_app
from routes.phone import phone_app

app = Flask(__name__)
app.config.from_envvar('ROBIN_CONFIG')

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(user_app)
app.register_blueprint(api_app)
app.register_blueprint(phone_app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def user_loader(user_id):
    return models.User.query.get(user_id)


@app.route('/')
def home():
    return render_template('landing.html')


@app.route('/person/lookup', methods=['GET', 'POST'])
def person_lookup():
    if request.method == 'GET':
        return render_template('lookup_user.html')

    person_id = request.form.get('person-id')
    last_name = request.form.get('last-name')

    person = models.Person.query.filter_by(id=person_id, last_name=last_name).first()
    if not person:
        flash('Unable to find person')
        return render_template('lookup_user.html')

    return redirect(url_for('person_view', id=person.id))


@app.route('/person/add')
def person_add():
    if request.method == 'GET':
        return render_template(
            'person_add.html',
            countries=data.get_countries(),
            languages=models.Language.query.all(),
        )

    return 'nyi'


@app.route('/person/<int:person_id>')
def person_view(person_id):
    person = models.Person.query.filter_by(id=person_id).first()
    if not person:
        flash('Unable to find person')
        return redirect(url_for('person_lookup'))

    return person['name']


@app.route('/service/history/add', methods=['GET', 'POST'])
def service_history_add():
    if request.method == 'GET':
        return render_template('service_history_add.html')
    return 'nyi'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
