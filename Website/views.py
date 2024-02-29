from flask import Blueprint, render_template
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)
    # the 'user=current_user' check's authentication

@views.route('/create-group')
@login_required
def create_group():
    return render_template("create-group.html", user=current_user)

@views.route('/initiative-tracker')
@login_required
def initiative_tracker():
    return render_template("initiative-tracker.html", user=current_user)