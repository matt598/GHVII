from flask import Blueprint, request, url_for
from tropo import Tropo, Result

import data


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

    countries = data.country_for_code(answer)

    t = Tropo()

    if not countries:
        t.ask(
            choices='[1-3 DIGITS]',
            name='code',
            say='Invalid country code, please try again.',
            timeout=5,
        )
        t.on(event='continue', next=url_for('phone.country'))
    elif len(countries) == 1:
        t.say('You selected')
        t.say(countries[0]['name'])
    else:
        t.ask(
            choices=', '.join(list(map(lambda country: country['name'], countries))),
            name='country',
            say='Please select one of the following countries.',
            timeout=5,
        )

    return t.RenderJson()
