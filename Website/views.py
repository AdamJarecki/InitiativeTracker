from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Group, db, Character


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return render_template("home.html", user=current_user)  
    # the 'user=current_user' check's authentication

@views.route('/create-group', methods=['GET', 'POST'])
@login_required
def create_group():
    if request.method == 'POST':
        group_name = request.form.get('group_name')
        if existing_group := Group.query.filter_by(group_name=group_name).first():
            flash('A group with this name already exists!', category='failure')
        else:
            is_player = bool(int(request.form.get('is_player')))
            # Create a new Group object
            new_group = Group(group_name=group_name, is_player=is_player, user_id=current_user.id)
            # Add the group to the database and commit changes
            db.session.add(new_group)
            db.session.commit()
            character_names = request.form.getlist('char_name[]')
            initiative_bonuses = request.form.getlist('initiative[]')

            for name, bonus in zip(character_names, initiative_bonuses):
                new_character = Character(character_name=name, initiative_bonus=bonus, group_id=new_group.id)
                db.session.add(new_character)

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