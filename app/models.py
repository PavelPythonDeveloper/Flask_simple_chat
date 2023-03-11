from app import db, login
from datetime import datetime
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    phone = db.Column(db.String)

    def __repr__(self):
        return f'User(id={self.id}, username={self.username})'


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f"Message(id={self.id}, " \
               f"sender_id={self.sender_id}, " \
               f"recipient_id={self.recipient_id}, " \
               f"body={self.body}, " \
               f"timestamp={self.timestamp})"
