# Import db from app
from app import db

# Import User model for manager and gardener
from app.mod_auth.models import User
# Import employeeInfo model for Manager and gardener
from app.mod_owner.models import employeeInfo

from markupsafe import escape

# Gives employee detials of all employees under an owner
def get_employee_list(ownerID):
    employee_id_list = employeeInfo.query.filter_by(ownerID = ownerID).all()
    employee_details_list = []
    
    for employee_id in employee_id_list:
        employee_details_list.append(User.get_details(User.query.filter_by(id = employee_id.eID).first()))
    
    return employee_details_list