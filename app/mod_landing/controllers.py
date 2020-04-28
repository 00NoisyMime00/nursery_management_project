# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
import datetime
# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_landing = Blueprint('landing', __name__, url_prefix='/')


# Set the route and accepted methods
@mod_landing.route('/', methods=['GET'])
@mod_landing.route('/index', methods=['GET'])
def index():
    print(session, str(datetime.datetime.now()))
    
    if('role' in session):
        if session['role'] == 0:
            return redirect(url_for('customer.index'))
        return render_template("landing/index.html", role = str(session['role']), user_name = session['user_name'])
    
    return render_template("landing/index.html", role = None)
