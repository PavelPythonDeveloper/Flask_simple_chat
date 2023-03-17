from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    messages = db.relationship('Message', backref='chat', lazy='dynamic')


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    phone = db.Column(db.String)
    password_hash = db.Column(db.String())

    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author',
                                    lazy='dynamic')

    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient',
                                        lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password=password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
