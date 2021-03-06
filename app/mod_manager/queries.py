# Import db from app
from app import db

from flask import session

from config import BASE_STATS_DIR

# Import User model for manager and gardener
from app.mod_auth.models import User

from app.mod_owner.models import nurseryStaff

from app.mod_gardener.models import seedTypeInfo, vendorSeedInfo, vendorInfo, plantInfo, plantStatus, costToRaise,\
                                   seedTypeInfo, seedBatchInfo, seedAvailable, gardenerOfPlant

from app.mod_manager.models import plantTypeInfo, plantImages

from app.mod_customer.models import complaints

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

def get_stats_for_seed_available(nID):
    plant_type_ids = plantTypeInfo.query.filter_by(nID=nID).all()
    index = []
    seed_type_total = []

    for plant_type_id in plant_type_ids:
        seed_type_ids = seedTypeInfo.query.filter_by(plantTypeID=plant_type_id.plantTypeID)\
            .join(seedBatchInfo, seedBatchInfo.seedTypeID==seedTypeInfo.seedTypeID)\
                .add_column(seedBatchInfo.seedBatchID).all()
        total_seeds = 0

        for seed_type in seed_type_ids:
            total_seeds += seedAvailable.query.filter_by(seedBatchID=seed_type.seedBatchID, nID=nID).first().quantity
        
        seed_type_total.append(total_seeds)
        index.append(plant_type_id.plantTypeName)
    
    a = pd.DataFrame({'Seeds Available':seed_type_total}, index=index)
    fig = a.plot.bar(rot=0).get_figure()
    fig.suptitle('Seeds Available Distribution', fontsize=18)
    plt.xlabel('Plant Type Name', fontsize=16)
    plt.ylabel('Number', fontsize=16)
    
    DIR = os.path.join(BASE_STATS_DIR, 'seedsAvailable')
    Path(DIR).mkdir(parents=True, exist_ok=True)
    IMG_PATH = os.path.join(DIR, '{nID}.png'.format(nID=nID))
    fig.savefig(IMG_PATH)
    
    return IMG_PATH.split('app/')[1]

def get_active_complaints(nID):
    active_complaints = complaints.query.filter_by(nID = nID).all()
    complaint_description = []

    for complaint in active_complaints:
        if complaint.complaintStatus == 0:
            description                     = {}
            description['pID']              = complaint.pID
            
            plant                           = plantInfo.query.filter_by(pID=description['pID']).first()
            plantType                       = plantTypeInfo.query.filter_by(plantTypeID=plant.plantTypeID).first()
            gardenerID                      = gardenerOfPlant.query.filter_by(pID=plant.pID).first()
            
            description['nID']              = nID
            description['description']      = complaint.description
            description['date']             = complaint.date.date()
            description['name']             = plantType.plantTypeName
            description['image']            = plantImages.query.filter_by(plantTypeID=plant.plantTypeID).first().imageLink
            description['complaintNumber']  = complaint.complaintNumber
            description['gardenerName']     = User.query.filter_by(id=gardenerID.eID).first().name
            description['gardenerID']       = gardenerID.eID

            complaint_description.append(description)
    
    return complaint_description

def resolve_complaint(complaintNumber):
    active_complaint = complaints.query.filter_by(complaintNumber=complaintNumber).first()

    if active_complaint != None and active_complaint.complaintStatus == 0:
        active_complaint.complaintStatus = 1
        db.session.commit()