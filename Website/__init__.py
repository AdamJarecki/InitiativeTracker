from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'long live the team'
    # create teh database using SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Initialize the DB
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Group, Character
    
    create_database(app)
    
    return app

def create_database(app):
    # check if database exists; if not, creates the database
    if not path.exists(f'website/{DB_NAME}'):
        db.create_all(app=app)
        print('Created Database!')