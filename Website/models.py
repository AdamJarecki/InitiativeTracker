from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), unique=True)
    is_player = db.Column(db.Boolean)
    characters = db.relationship('Character')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(50))
    initiative_bonus = db.Column(db.Integer)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    
    