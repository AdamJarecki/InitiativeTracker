from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# the User table is primarily used for registration to the website, as well as associating the enemy and player groups with the account.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    groups = db.relationship('Group')
    
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(128), unique=True)
    is_player = db.Column(db.Integer)
    characters = db.relationship('Character')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(128))
    initiative_bonus = db.Column(db.Integer)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship('Group', backref=db.backref('characers', lazy=True))

class SortingHatResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    strength = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    constitution = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    wisdom = db.Column(db.Integer)
    charisma = db.Column(db.Integer)
    charClass = db.Column(db.String(128))
    charSubClass = db.Column(db.String(128))
    charRace = db.Column(db.String(128))
    charBackground = db.Column(db.String(128))
    charAlignment = db.Column(db.String(128))
    skillProficiencies = db.Column(db.String(128))
    savingThrowProficiencies = db.Column(db.String(128))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
