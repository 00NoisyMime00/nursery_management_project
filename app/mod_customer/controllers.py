# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  abort

from markupsafe import escape

from app.mod_auth.controllers import check_logged_in

from app.mod_customer.queries import get_plants_available, get_complete_plant_info

import datetime
# Define the blueprint: 'customer', set its url prefix: app.url/auth
mod_customer = Blueprint('customer', __name__, url_prefix='/')


@mod_customer.route('/welcome', methods=['GET'])
def index():
    if(check_logged_in(0)):
        plants_list = get_plants_available()
        
        return render_template('landing/index.html', role=str(session['role']), plants_list=plants_list) 

@mod_customer.route('/view_plant_profile_customer', methods=['GET', 'POST'])
def view_plant_profile():
    if check_logged_in(0):
        if request.method == 'POST':
            if 'purchase' in request.form:
                pass
        if 'plantTypeID' in request.args:
            plantTypeID = request.args.get('plantTypeID')
            description = get_complete_plant_info(plantTypeID)
            return render_template('customer/view_plant_profile.html', role=str(session['role']), description=description)
    return redirect(url_for('landing.index')) 
    
@mod_customer.route('/view_orders', methods=['GET'])
def view_orders():
    print("pleasesse")
    if(check_logged_in(0)):
        return 'fjdkf'
	# 	return render_template("/customer/view_orders.html", role=str(session['role']))
	# else:
	# 	return redirect(url_for('landing.index'))


    
    
