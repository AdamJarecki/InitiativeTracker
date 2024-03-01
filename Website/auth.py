from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
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
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
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
            #login_user(user)  # , remember=True         
            flash('Account created!', category='success')

            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)

