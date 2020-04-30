# Import db from app
from app import db

# Import User model for manager and gardener
from app.mod_auth.models import User
# Import employeeInfo model for Manager and gardener
from app.mod_owner.models import employeeInfo, nurseryInfo, nurseryAddress, nurseryStaff

from app.mod_manager.models import plantTypeInfo

from app.mod_gardener.models import plantInfo, costToRaise

from app.mod_customer.models import plantsSold

from markupsafe import escape

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from config import BASE_STATS_DIR

import os
from pathlib import Path


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

def get_nurser_list(ownerID, pin='' ,city='',country=''):
    nursery_list = nurseryInfo.query.filter_by(ownerID=ownerID).all()
    nursery_details_list = []
    
    for nursery in nursery_list:

        if pin != '' and str(nurseryAddress.query.filter_by(nID=nursery.nID).first().get_pin_id()) == pin:
            nursery_details_list.append( nursery.get_details().__add__(nurseryAddress.query.filter_by(nID = nursery.nID).first().get_complete_address() ) )
        
        elif city != '' and (nurseryAddress.query.filter_by(nID=nursery.nID).first().get_city_id()).lower() == city.lower():
            nursery_details_list.append( nursery.get_details().__add__(nurseryAddress.query.filter_by(nID = nursery.nID).first().get_complete_address() ) )
        
        elif country != '' and (nurseryAddress.query.filter_by(nID=nursery.nID).first().get_country_id()).lower() == country.lower():
            nursery_details_list.append( nursery.get_details().__add__(nurseryAddress.query.filter_by(nID = nursery.nID).first().get_complete_address() ) )
        elif pin == '' and city == '' and country == "":
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

def get_stats_for_maintenance_cost(ownerID):
    nurseries_list = nurseryInfo.query.filter_by(ownerID=ownerID).all()
    cost_list = []
    index     = []

    for nursery in nurseries_list:
        index.append(nursery.nID)
        cost_list.append(nursery.maintenanceCost + nursery.labourCost)
    
    if cost_list == []:
        return
    a = pd.DataFrame({'cost':cost_list}, index=index)
    a = a.astype(float)
    fig = a.plot.bar(rot=0).get_figure()
    fig.suptitle('Maintenance and Labour Cost Distribution', fontsize=18)
    plt.xlabel('Nursery ID', fontsize=16)
    plt.ylabel('Total Cost', fontsize=16)
    
    DIR = os.path.join(BASE_STATS_DIR, 'maintenanceCost')
    Path(DIR).mkdir(parents=True, exist_ok=True)
    IMG_PATH = os.path.join(DIR, '{ownerID}.png'.format(ownerID=ownerID))
    fig.savefig(IMG_PATH)
    
    return IMG_PATH.split('app/')[1]

def get_stats_for_sales(ownerID):
    nurseries_list = nurseryInfo.query.filter_by(ownerID=ownerID).all()
    index = []
    cost_total = []
    selling_total = []

    for nursery in nurseries_list:
        plants = plantTypeInfo.query.filter_by(nID=nursery.nID).join(plantInfo, plantTypeInfo.plantTypeID==plantInfo.plantTypeID)\
                    .add_columns(plantInfo.pID).all()
        
        cost = 0
        # For getting total cost to raise till now
        for plant in plants:
            cost += costToRaise.query.filter_by(pID=plant.pID).first().cost
        cost_total.append(cost)

        sold = 0
        # For getting total plants sold
        plants_sold = plantsSold.query.filter_by(nID=nursery.nID).all()

        for plant in plants_sold:
            sold += plant.sellingPrice
        selling_total.append(sold)
        
        index.append(nursery.nID)
    
    a = pd.DataFrame({'Spent':cost_total, 'Earned':selling_total}, index=index)
    a = a.astype(float)
    fig = a.plot.bar(rot=0).get_figure()
    fig.suptitle('Total sales Distribution', fontsize=18)
    plt.xlabel('Nursery ID', fontsize=16)
    plt.ylabel('Amount', fontsize=16)
    
    DIR = os.path.join(BASE_STATS_DIR, 'totalSales')
    Path(DIR).mkdir(parents=True, exist_ok=True)
    IMG_PATH = os.path.join(DIR, '{ownerID}.png'.format(ownerID=ownerID))
    fig.savefig(IMG_PATH)
    
    return IMG_PATH.split('app/')[1]
        