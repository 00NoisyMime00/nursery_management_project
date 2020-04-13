# Import db from app
from app import db

from flask import session

# Import User model for manager and gardener
from app.mod_auth.models import User

from app.mod_owner.models import nurseryStaff

from app.mod_gardener.models import seedTypeInfo, vendorSeedInfo, vendorInfo

def get_gardeners(nID):
    employee_id_list = nurseryStaff.query.filter_by(nID=nID).all()
    gardener_details_list = []

    for employee in employee_id_list:
        if employee.eID != session['user_id']:
            gardener_details_list.append(User.get_details(User.query.filter_by(id = employee.eID).first()))
    return gardener_details_list

def get_vendors(plantTypeID, nID):
    seed_type_list = seedTypeInfo.query.filter_by(plantTypeID=plantTypeID).all()
    vendors_id_list = []

    for seedType in seed_type_list:
        vendors_id_list.append(vendorSeedInfo.query.filter_by(seedTypeID=seedType.seedTypeID).first())
    
    vendor_description_list = []
    for vendor in vendors_id_list:
        vendor_description = {}
        vendor_description['id']    = vendor.vendorID
        vendor_description['cost']  = vendor.seedCost
        vendor_description['name']  = vendorInfo.query.filter_by(vendorID=vendor.vendorID).first().vendorName
        vendor_description_list.append(vendor_description)

    return vendor_description_list