from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    last_message = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f'User {self.id}'
