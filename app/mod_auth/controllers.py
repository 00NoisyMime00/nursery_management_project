# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort,flash

from markupsafe import escape

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_auth.forms import LoginForm

# Import module models (i.e. User)
from app.mod_auth.models import User

from .forms import RegistrationForm,LoginForm

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and create users(YET TO BE IMPLEMENTED!)
@mod_auth.route('/signup/', methods=['GET', 'POST'])
def signup():
        # Check if not already signed in
    if 'user_id' in session:
        return redirect(url_for('landing.index'))

    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.name.data
        emailID = form.email.data
        password = form.password.data
        role = int(form.role.data)
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif User.query.filter_by(emailID = emailID
        ).first() is not None:
            error = 'User {} is already registered.'.format(username)
        if error is None:
            db.session.add(User(username, emailID, generate_password_hash(password), role))
            db.session.commit()
            return redirect(url_for('auth.signin'))

    return render_template('auth/signup.html',form=form,title = "Sign Up Page")


# Set the route and accepted methods
@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    # Check if not already signed in
    if 'user_id' in session:
        return redirect(url_for('landing.index'))

    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate():

        user = User.query.filter_by(emailID=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_name'] = escape(user.name)
            session['user_id'] = user.id
            session['role'] = user.role

            subpath = 'user'

            if(session['role'] == 0):
                role = 'customer'
            elif(session['role'] == 1):
                role = 'owner'
            elif(session['role'] == 2):
                role = 'manager'
            elif(session['role'] == 3):
                role = 'gardener'
            return redirect(url_for('{path}.index'.format(path = role)))
    return render_template("auth/signin.html", form=form)

# Checks if logged in before signing out
def check_logged_in(role = None):
    if('user_id' not in session):
        abort(401)
    if(role):
        if role != session['role']:
            print('herelrhelrl')
            return False
    return True


@mod_auth.route('/signout/', methods=['GET'])
def signout():
    if check_logged_in():
        session.clear()
    return redirect(url_for('landing.index'))
