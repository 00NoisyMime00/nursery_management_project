# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  abort

from markupsafe import escape

from app.mod_auth.controllers import check_logged_in

import datetime
# Define the blueprint: 'customer', set its url prefix: app.url/auth
mod_customer = Blueprint('customer', __name__, url_prefix='/')


# @mod_customer.route('/', methods=['GET'])
# @mod_customer.route('/<path:subpath>', methods=['GET'])

@mod_customer.route('/', methods=['GET'])
def index():
    if check_logged_in(0):
        return redirect(url_for('landing.index'))
    else:
        return redirect(url_for('landing.index'))
    
    

    
    
