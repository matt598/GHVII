from flask import Blueprint, redirect, request, url_for
from tropo import Tropo, Result

import data
from data import _


phone_app = Blueprint('phone', __name__, url_prefix='/phone')
sessions = {}


class CallSession:
    session_id = None

    def __init__(self, res: Result):
        self.session_id = res._sessionId #pylint: disable=W0212
        if self.session_id not in sessions:
            sessions[self.session_id] = {}

    def get(self, key: str, default=None):
        return sessions[self.session_id].get(key, default)

    def set(self, key: str, val):
        sessions[self.session_id][key] = val


@phone_app.route('/index', methods=['POST'])
def index():
    t = Tropo()
    t.ask(
        choices='[1-3 DIGITS]',
        name='code',
        say=_('Please enter your country code if you know it.'),
        timeout=2,
    )
    t.on(event='continue', next=url_for('phone.country'))
    t.on(event='incomplete', next=url_for('phone.language'))
    return t.RenderJson()


@phone_app.route('/language', methods=['POST'])
def language():
    supported_languages = ', '.join(['english'])

    t = Tropo()

    t.ask(
        choices=supported_languages,
        name='language',
        say=_('Which of the following languages would you prefer? %s') % supported_languages,
        timeout=10,
    )
    t.on(event='continue', next=url_for('phone.language_select'))

    return t.RenderJson()


@phone_app.route('/language/select', methods=['POST'])
def language_select():
    r = Result(request.data)
    s = CallSession(r)

    answer = r.getInterpretation()

    s.set('language', answer)

    return redirect(url_for('phone.hello'))


@phone_app.route('/country', methods=['POST'])
def country():
    r = Result(request.data)
    s = CallSession(r)

    answer = r.getInterpretation()

    countries = data.country_for_code(answer)

    t = Tropo()

    if not countries:
        t.ask(
            choices='[1-3 DIGITS]',
            name='code',
            say=_('Invalid country code, please try again.'),
            timeout=5,
        )
        t.on(event='continue', next=url_for('phone.country'))
    elif len(countries) == 1:
        t.say(_('You selected'))
        t.say(countries[0]['name'])
        s.set('country', countries[0]['name'])

        t.on(event='continue', next=url_for('phone.hello'))
    else:
        country_list = ', '.join(list(map(lambda country: country['name'], countries)))

        t.ask(
            choices=country_list,
            name='country',
            say=_('Please select one of the following countries. %s') % country_list,
            timeout=5,
        )

    return t.RenderJson()


@phone_app.route('/hello', methods=['POST'])
def hello():
    r = Result(request.data)
    s = CallSession(r)

    t = Tropo()

    s_country = s.get('country')
    s_language = s.get('language')

    if s_country:
        t.say('Country set to %s' % s_country)

    if s_language:
        t.say('Language set to %s' % s_language)

    return t.RenderJson()
