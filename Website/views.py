from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/create-group')
def create_group():
    return render_template("create-group.html")

@views.route('/initiative-tracker')
def initiative_tracker():
    return render_template("initiative-tracker.html")