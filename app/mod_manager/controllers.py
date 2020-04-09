# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort

from markupsafe import escape

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# import checked_logged_in function
from app.mod_auth.controllers import check_logged_in

# Import the database object from the main app module
from app import db

# Import User model for manager and gardener
from app.mod_auth.models import User
# Import employeeInfo model for Manager and gardener
from app.mod_owner.models import employeeInfo

# Import module forms
from app.mod_auth.forms import LoginForm

# Import module models (i.e. User)
from app.mod_auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_manager = Blueprint('manager', __name__, url_prefix='/')

@mod_manager.route('/', methods=['GET'])
def index():
    if check_logged_in(session['role']):
        return redirect(url_for('landing.index'))
    else:
        return redirect(url_for('landing.index'))

@mod_manager.route('/add_gardener', methods=['GET', 'POST'])
def add_gardener():
    if check_logged_in(2):
        if request.method == 'POST':
            username = request.form['name']
            emailID = request.form['emailID']
            password = request.form['password']
            role = 3
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            elif User.query.filter_by(emailID = emailID
            ).first() is not None:
                error = 'User {} is already registered.'.format(username)
            if error is None:
                temp = User(username, emailID, generate_password_hash(password), role)
                db.session.add(temp)
                db.session.commit()
                db.session.add(employeeInfo(temp.id , int(session['user_id'])))
                db.session.commit()
                print(temp, '<<<<<<<<<<<<<<')
                return redirect(url_for('manager.index'))

        return render_template('manager/add_gardener.html', role=str(session['role']))
    return redirect(url_for('landing.index'))
