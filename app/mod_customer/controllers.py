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
        plants_list = []
    	# plants_list = get_plants()
        return redirect(url_for('landing.index'),role = str(session['role']), plants_list = plants_list)
    else:
        return redirect(url_for('landing.index'))
    
    
@mod_customer.route('/view_orders', methods=['GET'])
def view_orders():
	if(check_logged_in(0)):
		return render_template("/customer/view_orders.html", role=str(session['role']))
	else:
		return redirect(url_for('landing.index'))


    
    
