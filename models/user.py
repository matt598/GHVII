import bcrypt

from db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person')

    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship('Service')

    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, compare_to) -> bool:
        return bcrypt.checkpw(compare_to.encode('utf-8'), self.password.encode('utf-8'))

    def is_active(self) -> bool:
        return True

    def get_id(self) -> int:
        return self.id

    def is_authenticated(self) -> bool:
        return True

    def is_anonymous(self) -> bool:
        return False
