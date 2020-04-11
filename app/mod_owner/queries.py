# Import db from app
from app import db

# Import User model for manager and gardener
from app.mod_auth.models import User
# Import employeeInfo model for Manager and gardener
from app.mod_owner.models import employeeInfo, nurseryInfo, nurseryAddress, nurseryStaff

from markupsafe import escape

# Gives employee detials of all employees under an owner
def get_employee_list(ownerID, status=''):
    manager_id_list = employeeInfo.query.filter_by(ownerID = ownerID).all()
    employee_id_list = manager_id_list

    unassigned_managers = []
    assigned_managers = []
    gardeners_list = []

    for manager in manager_id_list:
        if nurseryStaff.query.filter_by(eID=manager.eID).first() is not None:
            gardeners_list += employeeInfo.query.filter_by(ownerID = manager.eID).all()
            assigned_managers.append(manager)
        else:
            unassigned_managers.append(manager)
    
    if status == 'assigned':
        employee_id_list = assigned_managers + gardeners_list
    elif status == 'unassigned':
        employee_id_list = unassigned_managers
    else:
        employee_id_list = manager_id_list + gardeners_list

    employee_details_list = []
    
    for employee_id in employee_id_list:
        employee_details_list.append(User.get_details(User.query.filter_by(id = employee_id.eID).first()))
    
    return employee_details_list

def get_nurser_list(ownerID):
    nursery_list = nurseryInfo.query.filter_by(ownerID=ownerID).all()
    nursery_details_list = []

    for nursery in nursery_list:
        nursery_details_list.append( nursery.get_details().__add__(nurseryAddress.query.filter_by(nID = nursery.nID).first().get_complete_address() ) )
    
    return nursery_details_list

def check_manager_assigned(nID):
    employee_list = nurseryStaff.query.filter_by(nID=nID).all()

    for employee in employee_list:
        if User.query.get(employee.eID).role == 2:
           return True
    return False

def get_manager_id(nID):
    employee_list = nurseryStaff.query.filter_by(nID=nID).all()

    for employee in employee_list:
        if User.query.get(employee.eID).role == 2:
           return employee.eID