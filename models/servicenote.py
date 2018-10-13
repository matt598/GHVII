from db import db


class ServiceNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship('Service')

    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person')

    date = db.Column(db.Date)
    note = db.Column(db.String)
