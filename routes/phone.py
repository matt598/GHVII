from flask import Blueprint, request, url_for
from tropo import Tropo, Result


phone_app = Blueprint('phone', __name__, url_prefix='/phone')


@phone_app.route('/index', methods=['POST'])
def index():
    t = Tropo()
    t.ask(
        choices='[1-3 DIGITS]',
        name='code',
        say='Please enter your country code if you know it.',
        timeout=5,
    )
    t.on(event='continue', next=url_for('phone.country'))
    return t.RenderJson()


@phone_app.route('/country', methods=['POST'])
def country():
    r = Result(request.data)

    answer = r.getInterpretation()

    t = Tropo()
    t.say('You entered')
    t.say(answer, _as='DIGITS')

    return t.RenderJson()
