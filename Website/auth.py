from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout Page</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        if len(email) < 4:
            # require the email to be at least 4 characters
            # Should require it to be in an email like format
            flash('Invalid Email Format!', category='failure')
        elif len(firstName) < 2:
            flash('Name must be greater than 1 character!', category='failure')
        elif password1 != password2:
            flash('Passwords don\'t match!', category='failure')
        elif len(password1) < 7:
            flash('Password must be at least 8 characters!', category='failure')
        else:
            # add user to database
            flash('Account created!', category='success')
        
    return render_template("signup.html")

