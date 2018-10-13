from db import db


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    location = db.Column(db.String)
    image = db.Column(db.String)
    description = db.Column(db.String)
    website = db.Column(db.String)
    phone = db.Column(db.String)
    primaryCountry = db.Column(db.String)

    service_type_id = db.Column(db.Integer, db.ForeignKey('service_type.id'), nullable=False)
    service_type = db.relationship('ServiceType')
