from flask import Blueprint, request, render_template, redirect, url_for, flash
from dateutil.parser import parse
from datetime import datetime

from db import db
import data
import models

person_app = Blueprint('person', __name__, url_prefix='/person')


@person_app.route('/find', methods=['GET', 'POST'])
def find():
    if request.method == 'GET':
        return render_template('lookup_user.html')

    person_id = request.form.get('person-id')
    last_name = request.form.get('last-name')

    person = models.Person.query.filter_by(id=person_id, last_name=last_name).first()
    if not person:
        flash('Unable to find person')
        return render_template('lookup_user.html')

    return redirect(url_for('.view', person_id=person.id))


@person_app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template(
            'person_add.html',
            countries=data.get_countries(),
            languages=models.Language.query.all(),
        )

    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    country = request.form.get('country')
    language = request.form.get('language')

    person = models.Person()
    person.first_name = first_name
    person.last_name = last_name
    person.email = email
    person.phone = phone
    person.origin_country = country

    language = models.Language.query.get(language)
    print(language)
    person.languages.append(language)

    db.session.add(person)
    db.session.commit()

    return redirect(url_for('.view', person_id=person.id))


@person_app.route('/<int:person_id>')
def view(person_id):
    person = models.Person.query.get(person_id)
    if not person:
        flash('Unable to find person')
        return redirect(url_for('.find'))

    return render_template('person_view.html', person=person)


@person_app.route('/note', methods=['POST'])
def note():
    person = request.form.get('person')
    service = request.form.get('service')
    note = request.form.get('note')

    service_note = models.ServiceNote()
    service_note.note = note
    service_note.person_id = person
    service_note.service_id = service
    service_note.date = datetime.now()

    db.session.add(service_note)
    db.session.commit()

    return redirect(url_for('.view', person_id=person))


@person_app.route('/history', methods=['POST'])
def history():
    person = request.form.get('person')
    service = request.form.get('service')

    started_at = request.form.get('started-at')
    ended_at = request.form.get('ended-at')
    case_notes = request.form.get('case-notes')

    history = models.ServiceHistory()
    history.person_id = person
    history.service_id = service
    try:
        history.started_at = parse(started_at)
    except ValueError:
        print('no started at')
        history.started_at = None
    try:
        history.ended_at = parse(ended_at)
    except ValueError:
        print('no ended at')
        history.ended_at = None
    history.case_notes = case_notes

    db.session.add(history)
    db.session.commit()

    return redirect(url_for('.view', person_id=person))


@person_app.route('/appointment', methods=['POST'])
def appointment():
    person = request.form.get('person')
    service = request.form.get('service')
    at = request.form.get('date')
    message = request.form.get('message')

    appointment = models.ServiceReminder()
    appointment.person_id = person
    appointment.service_id = service
    try:
        appointment.date = parse(at)
    except ValueError:
        appointment.date = None
    appointment.message = message

    db.session.add(appointment)
    db.session.commit()

    return redirect(url_for('.view', person_id=person))
