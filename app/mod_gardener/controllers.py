# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort

from markupsafe import escape 
# Import these tables
from app.mod_gardener.models import seedTypeInfo, seedBatchInfo, plantInfo, plantTypeInfo, costToRaise
# Import nurseryStaff table
from app.mod_owner.models import nurseryStaff

from app.mod_manager.models import plantTypeInfo

# import checked_logged_in function
from app.mod_auth.controllers import check_logged_in

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
    return redirect(url_for('landing.index'))