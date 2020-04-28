# Import db from app
from app import db

from flask import session

from config import BASE_STATS_DIR

# Import User model for manager and gardener
from app.mod_auth.models import User

from app.mod_owner.models import nurseryStaff

from app.mod_gardener.models import seedTypeInfo, vendorSeedInfo, vendorInfo, plantInfo, plantStatus, costToRaise

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

import os
from pathlib import Path

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

def get_stats_for_selling_price(plantTypeID):
    grown_plants = plantInfo.query.filter_by(plantTypeID=plantTypeID, plantStatus=plantStatus.GROWN).all()
    cost_list = []
    
    for plant in grown_plants:
        description = {}
        description['id'] = plant.pID
        description['costToRaise'] = costToRaise.query.filter_by(pID=plant.pID).first().cost
        cost_list.append(description)
    if cost_list == []:
        return ''
    a = pd.DataFrame(cost_list)
    fig = a.plot(x='id', y='costToRaise', kind='scatter').get_figure()
    fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    fig.gca().yaxis.set_major_locator(MaxNLocator(float=True))
    fig.suptitle('Cost To Raise Distribution', fontsize=20)
    plt.xlabel('ID', fontsize=16)
    plt.ylabel('Cost To Raise', fontsize=16)
    
    DIR = os.path.join(BASE_STATS_DIR, 'costToRaise')
    Path(DIR).mkdir(parents=True, exist_ok=True)
    IMG_PATH = os.path.join(DIR, '{plantTypeID}.png'.format(plantTypeID=plantTypeID))
    fig.savefig(IMG_PATH)
    
    return IMG_PATH.split('app/')[1]
    