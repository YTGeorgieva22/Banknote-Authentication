from __init__ import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username =db.Column(db.String(80), unique=True, nullable=False)
    __password = db.Column(db.String(80), nullable=False)