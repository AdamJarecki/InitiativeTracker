from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)
    # the 'user=current_user' check's authentication

@views.route('/create-group', methods=['GET', 'POST'])
@login_required
def create_group():
    if request.method =='POST':
        group_name = request.form.get('group_name')
        is_player = request.form.get('is_player')
        initiative_bonus = request.form.get('initiative_bonus')
        
    
    '''if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if user := User.query.filter_by(email=email).first():
            flash('Email already registered.', category='failure')
        elif len(email) < 4:
            # require the email to be at least 4 characters
            # Should require it to be in an email like format
            flash('Invalid Email Format!', category='failure')
            # for some reason, first_name is throwing an error calling it a 'NoneType' and won't accept the len function; so, it gone
        elif password1 != password2:
            flash('Passwords don\'t match!', category='failure')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters!', category='failure')
        else:
            # add user to database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)            
            flash('Account created!', category='success')

            return redirect(url_for('views.home'))    '''
    
    
    return render_template("create-group.html", user=current_user)

@views.route('/initiative-tracker')
@login_required
def initiative_tracker():
    return render_template("initiative-tracker.html", user=current_user)