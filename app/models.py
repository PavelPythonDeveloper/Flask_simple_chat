from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


chat_user = db.Table('chat_user',
                     db.Column('chat_id', db.Integer(), db.ForeignKey('chat.id')),
                     db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
                     )


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    messages = db.relationship('Message', backref='chat', lazy='dynamic')

    def __repr__(self):
        return f'Chat(id={self.id}, users={self.users}, messages_id={[message.id for message in self.messages]})'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String())

    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author',
                                    lazy='dynamic')

    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient',
                                        lazy='dynamic')

    chats = db.relationship('Chat', secondary=chat_user, backref='users')

    avatar_path = db.Column(db.String, index=True, unique=True)

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
    chat_id = db.Column(db.Integer(), db.ForeignKey('chat.id'))

    def __repr__(self):
        return f"Message(id={self.id}, " \
               f"sender_id={self.sender_id}, " \
               f"recipient_id={self.recipient_id}, " \
               f"body={self.body}, " \
               f"timestamp={self.timestamp})"
