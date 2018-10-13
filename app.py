from flask import Flask
from flask_login import current_user

from db import db
from login import login_manager
import models

from routes.user import user_app
from routes.api import api_app

app = Flask(__name__)
app.config.from_envvar('ROBIN_CONFIG')

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(user_app)
app.register_blueprint(api_app)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
