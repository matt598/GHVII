from flask import Flask, render_template, request

from db import db
from login import login_manager
import models

from routes.user import user_app
from routes.api import api_app
from routes.phone import phone_app
from routes.person import person_app
from routes.profile import profile_app

app = Flask(__name__)
app.config.from_envvar('ROBIN_CONFIG')

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(user_app)
app.register_blueprint(api_app)
app.register_blueprint(phone_app)
app.register_blueprint(person_app)
app.register_blueprint(profile_app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def user_loader(user_id):
    return models.User.query.get(user_id)


@app.route('/')
def home():
    return render_template('landing.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/service/history/add', methods=['GET', 'POST'])
def service_history_add():
    if request.method == 'GET':
        return render_template('service_history_add.html')
    return 'nyi'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
