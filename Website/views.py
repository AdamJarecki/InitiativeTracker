from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Group, db


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)
    # the 'user=current_user' check's authentication

@views.route('/create-group', methods=['GET', 'POST'])
@login_required
def create_group():
    if request.method == 'POST':
        group_name = request.form.get('group_name')
        is_player = request.form.get('is_player')
        initiative_bonus = request.form.get('initiative_bonus')
        
        # Create a new Group object
        new_group = Group(group_name=group_name, is_player=is_player, user_id=current_user.id)
        
        # Add the group to the database and commit changes
        db.session.add(new_group)
        db.session.commit()
        
        flash('Group created successfully!', category='success')
        
        # Redirect to the initiative tracker page
        return redirect(url_for('views.initiative_tracker'))

    return render_template("create-group.html", user=current_user)

@views.route('/initiative-tracker')
@login_required
def initiative_tracker():
    groups = Group.query.filter_by(user_id=current_user.id).all()
    return render_template("initiative-tracker.html", user=current_user)