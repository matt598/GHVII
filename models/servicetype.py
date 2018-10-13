from db import db


class ServiceType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    image = db.Column(db.String)
    description = db.Column(db.String)
