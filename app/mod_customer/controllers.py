# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
                  abort

from markupsafe import escape

from app import db

from app.mod_auth.controllers import check_logged_in

from app.mod_customer.queries import get_plants_available, get_complete_plant_info, get_order_history, get_cart_items,\
                                        get_nursery_for_plant

from app.mod_customer.models import plantsSold, transactionInfo, cart

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
        if request.method == 'POST' and 'id' in request.form:
            plantTypeID                 = int(request.form.get('id'))
            description                 = get_complete_plant_info(plantTypeID)

            if description['quantity'] == 0:
                return redirect(url_for('customer.view_plant_profile'))

            plant                         = plantInfo.query\
                                            .join(plantsAvailable, plantInfo.pID==plantsAvailable.pID)\
                                            .first()

            plantAvailableColumn         = plantsAvailable.query.filter_by(pID=plant.pID).first()
            nID                          = description['nID']
            sellingPrice                 = description['sellingPrice']
            
            if 'purchase' in request.form:
                
                transaction                  = transactionInfo(session['user_id'])
                
                db.session.add(transaction)
                db.session.commit()
                
                db.session.add(plantsSold(transaction.transactionID, plant.pID, nID, sellingPrice))
                plant.plantStatus = plantStatus.SOLD
                db.session.delete(plantAvailableColumn)
                db.session.commit()
            
            if 'add_to_cart' in request.form:

                db.session.add(cart(session['user_id'], plant.pID))
                db.session.delete(plantAvailableColumn)
                db.session.commit()
                

        if 'plantTypeID' in request.args:
            plantTypeID = request.args.get('plantTypeID')
            description = get_complete_plant_info(plantTypeID)
            return render_template('customer/view_plant_profile.html', role=str(session['role']), description=description)
    return redirect(url_for('landing.index')) 
    
@mod_customer.route('/view_order_history', methods=['GET'])
def view_order_history():
    if(check_logged_in(0)):
        orders = get_order_history(session['user_id'])
        return render_template('customer/view_order_history.html', role=str(session['role']), userID=session['user_id'], orders=orders)
    return redirect(url_for('landing.index'))

@mod_customer.route('/view_cart', methods=['GET', 'POST'])
def view_cart():
    if check_logged_in(0):
        items = get_cart_items(session['user_id'])
        return render_template('customer/view_cart.html', role=str(session['role']), items=items)
    return redirect(url_for('landing.index'))

@mod_customer.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if check_logged_in(0) and 'id' in request.form:
        pID = int(request.form.get('id'))
        cart_item = cart.query.filter_by(customerID=session['user_id'], pID=pID).first()
        nID = get_nursery_for_plant(pID)
        
        db.session.delete(cart_item)
        db.session.add(plantsAvailable(pID, nID))
        db.session.commit()

        return redirect(url_for('customer.view_cart'))
    return redirect(url_for('landing.index'))

@mod_customer.route('/checkout_cart', methods=['POST'])
def checkout_cart():
    if check_logged_in(0):
        items = get_cart_items(session['user_id'])
        
        for item in items:
            cart_item = cart.query.filter_by(customerID=session['user_id'], pID=item['id']).first()
            transaction                  = transactionInfo(session['user_id'])
                
            db.session.add(transaction)
            db.session.delete(cart_item)
            db.session.commit()
            
            plant = plantInfo.query.filter_by(pID=item['id']).first()
            db.session.add(plantsSold(transaction.transactionID, item['id'], item['nID'], item['sellingPrice']))
            plant.plantStatus = plantStatus.SOLD
            db.session.commit()
        
    return redirect(url_for('landing.index'))