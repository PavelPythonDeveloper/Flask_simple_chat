from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    phone = db.Column(db.String)

    def __repr__(self):
        return f'User(id={self.id}, username={self.username})'