# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort

from app import db

from markupsafe import escape 
# Import these tables
from app.mod_gardener.models import seedTypeInfo, seedBatchInfo, plantInfo, plantTypeInfo, costToRaise, seedAvailable\
    ,plantInfo, gardenerOfPlant, costToRaise, plantStatus, plantsAvailable
# Import nurseryStaff table
from app.mod_owner.models import nurseryStaff

from app.mod_manager.models import plantTypeInfo

from app.mod_gardener.queries import get_complete_plant_description, get_seeds_to_sow, get_plants_assigned, get_plant_profile

# import checked_logged_in function
from app.mod_auth.controllers import check_logged_in

import decimal

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_gardener = Blueprint('gardener', __name__, url_prefix='/')

@mod_gardener.route('/', methods=['GET'])
def index():
    if check_logged_in(session['role']):
        return redirect(url_for('landing.index'))
    else:
        return redirect(url_for('landing.index'))

@mod_gardener.route('/view_plant_types', methods=['GET'])
def view_plant_types():
    if check_logged_in(3):
        nID = nurseryStaff.query.filter_by(eID=session['user_id']).first().nID
        plant_type_list = plantTypeInfo.query.filter_by(nID=nID).all()
        plant_description_list = []
        for plant in plant_type_list:
            plant_description = get_complete_plant_description(plant.plantTypeID)
            plant_description['seeds_list']  = get_seeds_to_sow(plant.plantTypeID)
            plant_description_list.append(plant_description)
        
        return render_template('gardener/view_plant_types.html', role=str(session['role']), plant_type_list=plant_description_list)

    return redirect(url_for('landing.index'))

@mod_gardener.route('/sow_seeds', methods=['POST'])
def sow_seeds():
    if check_logged_in(3) and 'checkbox' in request.form:
        data = request.form.getlist('checkbox')

        for batch in data:
            seedBatchID = int(batch.split('_')[0])
            plantTypeID = int(batch.split('_')[1])
           
            quantity = request.form["quantity"+str(seedBatchID)]
            if quantity != '':
                quantity = int(quantity)
                # Check if quantity <= availability
                seedBatch = seedAvailable.query.filter_by(seedBatchID=seedBatchID).first()
                if quantity <= seedBatch.quantity:
                    # Update seed available
                    seedBatch.quantity -= quantity

                    seedBatchInfoObject = seedBatchInfo.query.filter_by(seedBatchID=seedBatchID).first()
                    for i in range(0, quantity):
                        plant = plantInfo(plantTypeID, seedBatchID, seedTypeInfo.query.filter_by(seedTypeID=seedBatchInfoObject.seedTypeID).first().plantColor, plantStatus.GROWING)
                        db.session.add(plant)
                        db.session.commit()
                        # Add value to cost to raise
                        db.session.add(costToRaise(plant.pID, (seedBatchInfoObject.batchCost)/1000))
            
                        # Update gardener of plant
                        gardener = gardenerOfPlant(plant.pID, session['user_id'])
                        db.session.add(gardener)
                        db.session.commit()
    return redirect(url_for('landing.index'))

@mod_gardener.route('/view_plants_assigned', methods=['GET'])
def view_plants_assigned():
    if check_logged_in(3):
        plants_list = get_plants_assigned(session['user_id'])
        return render_template('gardener/view_plants_assigned.html', role=str(session['role']), plants_list=plants_list)
    return redirect(url_for('landing.index'))

@mod_gardener.route('/change_status')
def change_status():
    if check_logged_in(3):
        nID = nurseryStaff.query.filter_by(eID=session['user_id']).first().nID
        pID = request.args.get('id', default='')
        status = request.args.get('status', default='')

        possible_status = ['growing', 'grown', 'sold', 'dead', 'needs_attention']
        if pID != '' and status in possible_status:
            plant = plantInfo.query.filter_by(pID=int(pID)).first()
            if status == 'growing':
                plant.plantStatus = plantStatus.GROWING
            elif status == 'grown':
                db.session.add(plantsAvailable(plant.pID, nID))
                db.session.commit()
                plant.plantStatus = plantStatus.GROWN
            elif status == 'sold':
                plant.plantStatus = plantStatus.SOLD
            elif status == 'dead':
                plant.plantStatus = plantStatus.DEAD
            elif status == 'needs_attention':
                plant.plantStatus = plantStatus.NEEDS_ATTENTION
            db.session.commit()
        return redirect(url_for('gardener.view_plants_assigned'))
    return redirect(url_for('landing.index'))

@mod_gardener.route('/view_plant_profile', methods=['GET'])
def view_plant_profile():
    if check_logged_in(3):
        pID = request.args.get('pID', default='')
        print(pID)
        if pID != '':
            pID = int(pID)
            description = get_plant_profile(pID)
            if description['gardenerID'] == session['user_id']:
                return render_template('gardener/view_plant_profile.html', description=description, role=str(session['role']))
    return redirect(url_for('landing.index'))

@mod_gardener.route('/update_cost_to_raise', methods=['POST'])
def update_cost_to_raise():
    if check_logged_in(3) and 'reason' in request.form and 'cost' in request.form:
        pID     = int(request.form.get('id'))
        reason  = request.form.get('reason')
        cost    = decimal.Decimal(request.form.get('cost'))

        plant       = costToRaise.query.filter_by(pID=pID).first()
        plant.cost  += cost
        db.session.commit()
        return redirect(url_for('gardener.view_plants_assigned'))
    return redirect(url_for('landing.index'))