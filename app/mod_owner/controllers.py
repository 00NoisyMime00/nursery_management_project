# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  abort
# Import db from app
from app import db

# Import User model for manager and gardener
from app.mod_auth.models import User
# Import employeeInfo model for Manager and gardener
from app.mod_owner.models import employeeInfo

from markupsafe import escape


# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# import checked_logged_in function
from app.mod_auth.controllers import check_logged_in


# Define the blueprint: 'customer', set its url prefix: app.url/auth
mod_owner = Blueprint('owner', __name__, url_prefix='/')


# @mod_owner.route('/', methods=['GET'])
# @mod_owner.route('/<path:subpath>', methods=['GET'])

@mod_owner.route('/', methods=['GET'])
def index():
    if check_logged_in(session['role']):
        return redirect(url_for('landing.index'))
    else:
        return redirect(url_for('landing.index'))

@mod_owner.route('/add_manager', methods=['GET', 'POST'])
def add_manager():
    print(check_logged_in(1))
    if check_logged_in(1):
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
                error = 'User {} is already registered.'.format(username)
            if error is None:
                temp = User(username, emailID, generate_password_hash(password), role)
                db.session.add(temp)
                db.session.commit()
                db.session.add(employeeInfo(temp.id , int(session['user_id'])))
                db.session.commit()
                return redirect(url_for('owner.index'))

        return render_template('owner/add_employee.html', role = session['role'])
    return redirect(url_for('landing.index'))

    @mod_owner.route('/view_employee', methods=['GET'])
    def view_employee():
        pass
    
