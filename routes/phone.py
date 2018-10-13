from flask import Blueprint
from tropo import Tropo

phone_app = Blueprint('phone', __name__, url_prefix='/phone')


@phone_app.route('/index')
def index():
    t = Tropo()
    t.say('Hello, world!')
    return t.RenderJson()
