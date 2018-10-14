from db import db


class ServiceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', backref='history')

    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship('Service')

    started_at = db.Column(db.Date)
    ended_at = db.Column(db.Date)

    user_feedback = db.Column(db.String)
    case_notes = db.Column(db.String)
