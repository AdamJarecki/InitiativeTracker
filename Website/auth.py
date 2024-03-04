from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re


auth = Blueprint('auth', __name__)

# login does exactly what you'd expect; it logs the user in. 
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # this makes sure the browser is in the right state
    if request.method == 'POST':
        # these pull the appropriate variables to verify
        email = request.form.get('email')
        password = request.form.get('password')
        # this part verifies the information submitted is correct; it checks for if the user exists first (via email address), and then verifies the password is correct.
        if user := User.query.filter_by(email=email).first():
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user)  #, remember=True
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password; try again.', category='failure')
        else:
            flash('Email does not exist.', category='failure')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    # this pulls directly from flask_login to do what it needs to do. 
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        lowercase_check = re.compile(r'[a-z]')
        uppercase_check = re.compile(r'[A-Z]')
        symbol_check = re.compile(r'[\W_]')  # \W matches any non-word character, _ is included to consider it as a symbol

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
        elif not (lowercase_check.search(password1) and uppercase_check.search(password1) and symbol_check.search(password1)):
                # Check if the password meets the complexity requirements
                flash('Password must contain at least one lowercase letter, one uppercase letter, and one symbol.', category='failure')            
        else:
            # add user to database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            #login_user(user, remember=True)  # Wasn't working for some reason, so I just removed it.         
            flash('Account created!', category='success')

            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)

