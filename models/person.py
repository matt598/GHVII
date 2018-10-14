from db import db
from models.servicenote import ServiceNote


language_association = db.Table(
    'language_association',
    db.Column('person_id', db.Integer, db.ForeignKey('person.id'), primary_key=True),
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'), primary_key=True),
)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    origin_country = db.Column(db.String)

    languages = db.relationship('Language', secondary=language_association)

    def service_notes(self, service: int):
        return ServiceNote.query.filter_by(service_id=service).all()
