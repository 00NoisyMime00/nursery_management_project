# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  abort

from markupsafe import escape

from app import db

from app.mod_auth.controllers import check_logged_in

from app.mod_customer.queries import get_plants_available, get_complete_plant_info

from app.mod_customer.models import plantsSold, transactionInfo

from app.mod_gardener.models import plantInfo, plantStatus, plantsAvailable

from app.mod_gardener.models import plantTypeInfo

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
            if 'purchase' in request.form and 'id' in request.form:
                plantTypeID                 = int(request.form.get('id'))
                description                 = get_complete_plant_info(plantTypeID)

                if description['quantity'] == 0:
                    return redirect(url_for('customer.view_plant_profile'))

                plant                       = plantInfo.query.filter_by(plantTypeID=plantTypeID, plantStatus=plantStatus.GROWN).first()

                plantAvailableColumn         = plantsAvailable.query.filter_by(pID=plant.pID).first()
                nID                          = description['nID']
                sellingPrice                 = description['sellingPrice']
                transaction                  = transactionInfo(session['user_id'])
                
                db.session.add(transaction)
                db.session.commit()
                
                db.session.add(plantsSold(transaction.transactionID, plant.pID, nID, sellingPrice))
                plant.plantStatus = plantStatus.SOLD
                db.session.delete(plantAvailableColumn)
                db.session.commit()
            
            if 'add_to_cart' in request.form:
                print(request.form, "<<<<<<<<<<")
                

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


    
    
