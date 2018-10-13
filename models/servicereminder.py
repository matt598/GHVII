from db import db


class ServiceReminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    date = db.Column(db.Date)
    message = db.Column(db.String)
