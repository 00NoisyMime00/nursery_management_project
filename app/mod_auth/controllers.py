# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort

from markupsafe import escape

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_auth.forms import LoginForm

# Import module models (i.e. User)
from app.mod_auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and create users(YET TO BE IMPLEMENTED!)
@mod_auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    # admin = User(name='admin', email='admin@code.com', password='admin@123')
    # admin.role = 1
    # admin.status = 1
    # db.session.add(admin)
    # db.session.commit()
    # print(User.query.all())
    # print(db.engine.execute("select * from auth_user"))
    # return render_template("auth/signup.html")
    if request.method == 'POST':
        username = request.form['name']
        emailID = request.form['emailID']
        password = request.form['password']
        role = request.form['role']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif User.query.filter_by(emailID = emailID
        ).first() is not None:
        # elif db.execute(
        #     'SELECT id FROM user WHERE username = ?', (username,)
        # ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            # db.execute(
            #     'INSERT INTO user (username, password) VALUES (?, ?)',
            #     (username, generate_password_hash(password))
            # )
            db.session.add(User(username, emailID, generate_password_hash(password), role))
            db.session.commit()
            return redirect(url_for('auth.signin'))

        flash(error)

    return render_template('auth/signup.html')


# Set the route and accepted methods
@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():

    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():

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
