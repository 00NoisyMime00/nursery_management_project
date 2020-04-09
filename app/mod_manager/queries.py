# Import db from app
from app import db

from flask import session

# Import User model for manager and gardener
from app.mod_auth.models import User

from app.mod_owner.models import nurseryStaff

def get_gardeners(nID):
    employee_id_list = nurseryStaff.query.filter_by(nID=nID).all()
    gardener_details_list = []

    for employee in employee_id_list:
        if employee.eID != session['user_id']:
            gardener_details_list.append(User.get_details(User.query.filter_by(id = employee.eID).first()))
    return gardener_details_list