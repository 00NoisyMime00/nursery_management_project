# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  abort

from markupsafe import escape

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

@mod_owner.route('/add_manager', methods=['GET'])
def add_manager():
    print(check_logged_in(1))
    if check_logged_in(1):
        return 'hey'
    return redirect(url_for('landing.index'))
    
