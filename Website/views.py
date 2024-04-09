from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
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
        if existing_group := Group.query.filter_by(
            group_name=group_name
        ).first():
            flash('A group with this name already exists!', category='failure')
        else:
            is_player = bool(int(request.form.get('is_player')))
            # Create a new Group object
            new_group = Group(group_name=group_name, is_player=is_player, user_id=current_user.id)
            # Add the group to the database and commit changes
            db.session.add(new_group)
            db.session.commit()
            # The variable names that these are pulling from ('char_name[]' and 'initiative[]') are pulled from the create-group.html file.
            character_names = request.form.getlist('char_name[]')
            initiative_bonuses = request.form.getlist('initiative[]')
            # this adds the players to the DB, by looping through all the inputs
            for name, bonus in zip(character_names, initiative_bonuses):
                new_character = Character(character_name=name, initiative_bonus=bonus, group_id=new_group.id)
                db.session.add(new_character)
            # this one commit's the new players after adding them. I'm not sure if I need both db.session.commit() functions, but it feels safer to keep both
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

@views.route('/edit-group', methods=['GET', 'POST'])
@login_required
def edit_group():
    groups = Group.query.filter_by(user_id=current_user.id).all()  # Fetch all groups for the dropdown

    if request.method == 'POST':
        # Retrieve the selected group's ID from the form data
        selected_group_id = request.form.get('group')
        if group := Group.query.get(selected_group_id):
            # Retrieve character names and initiative bonuses from the form
            character_names = request.form.getlist('char_name[]')
            initiative_bonuses = request.form.getlist('initiative[]')

            # Add the new characters to the DB, associating them with the selected group
            for name, bonus in zip(character_names, initiative_bonuses):
                new_character = Character(character_name=name, initiative_bonus=bonus, group_id=group.id)
                db.session.add(new_character)

            db.session.commit()  # Commit once after adding all new characters

            flash('Group updated successfully!', category='success')
        else:
            flash('Selected group not found.', category='error')

    return render_template("edit-group.html", groups=groups, user=current_user)


@views.route('/get-characters', methods=['GET', 'POST'])
@login_required
def get_characters():
    if group_id := request.args.get('group_id'):
        characters = Character.query.filter_by(group_id=group_id).all()
        character_data = [{'id': char.id, 'name': char.character_name, 'initiative_bonus': char.initiative_bonus} for char in characters]
        return jsonify({'characters': character_data})
    return jsonify({'characters': []})

@views.route('/delete-character', methods=['POST'])
@login_required
def delete_character():
    character_id = request.form.get('character_id')
    if character := Character.query.get(character_id):
        db.session.delete(character)
        db.session.commit()
        return jsonify({'success': 'Character deleted successfully'}), 200
    return jsonify({'error': 'Character not found'}), 404


@views.route('/delete-group/<int:group_id>', methods=['DELETE'])
@login_required
def delete_group(group_id):
    group = Group.query.get_or_404(group_id)
    if group.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(group)
    db.session.commit()
    return jsonify({'success': 'Group deleted successfully'}), 200

@views.route('/sorting-hat')
@login_required
def sorting_hat():
    return render_template("sorting-hat.html", user=current_user)

@views.route('/sorting-hat-output')
@login_required
def sorting_hat_output():
    character_info = {
        'class': 'Rogue',
        'archetype': 'Thief',
        'race': 'Elf',
        'skills': 'Stealth, Sleight of Hand, Acrobatics, Perception, Investigation, Insight, Persuasion, Deception, Intimidation, Performance, Animal Handling, Survival, Nature, History, Arcana, Religion, Medicine, Athletics, and Persuasion.'
    }
    return render_template("sorting-hat-output.html", user=current_user)