from app import db

from app.mod_manager.models import plantTypeInfo, plantImages, plantTypeUses, plantTypeDescription

from app.mod_gardener.models import seedTypeInfo, seedBatchInfo, seedAvailable, vendorSeedInfo\
    , vendorInfo, gardenerOfPlant, plantInfo, costToRaise, plantStatus

from app.mod_auth.models import User

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from config import BASE_STATS_DIR

import os
from pathlib import Path

def get_complete_plant_description(pID):
    description = {}
    
    plant = plantTypeInfo.query.filter_by(plantTypeID=pID).first()
    description['id']           = pID
    description['name']         = plant.plantTypeName
    description['sellingPrice'] = plant.sellingPrice
    description['image']        = plantImages.query.filter_by(plantTypeID=plant.plantTypeID).first().imageLink
    
    plantUses = plantTypeUses.query.filter_by(plantTypeID=plant.plantTypeID).first()
    description['uses']     = []
    if plantUses.cosmetic == True:
        description['uses'].append('cosmetic')
    if plantUses.medicinal == True:
        description['uses'].append('medicinal')
    if plantUses.decorative == True:
        description['uses'].append('decorative')
    if plantUses.edible == True:
        description['uses'].append('edible')
    
    description['seedsAvailable'] = 0
    seed_type_list = seedTypeInfo.query.filter_by(plantTypeID=plant.plantTypeID).all()
    for seedType in seed_type_list:
        seed_batch_list = seedBatchInfo.query.filter_by(seedTypeID=seedType.seedTypeID).all()
        for seedBatch in seed_batch_list:
            description['seedsAvailable'] += seedAvailable.query.filter_by(seedBatchID=seedBatch.seedBatchID, nID=plant.nID).first().quantity
    
    return description

def get_seeds_to_sow(plantTypeID):
    seed_types = seedTypeInfo.query.filter_by(plantTypeID=plantTypeID).all()
    seed_description_list = []

    for seed in seed_types:
        seed_description = {}
        seedBatch                       = seedBatchInfo.query.filter_by(seedTypeID=seed.seedTypeID).first()
        if seedBatch == None:
            continue
        vendor = vendorSeedInfo.query.filter_by(seedTypeID=seed.seedTypeID).first()
        seed_description['vendor_name'] = vendorInfo.query.filter_by(vendorID=vendor.vendorID).first().vendorName
        seed_description['cost']        = vendor.seedCost
        
        seed_description['id']          = seedBatch.seedBatchID
        seed_description['date']        = seedBatch.dateOfPurchase.date()
        seed_description['batch_size']  = seedAvailable.query.filter_by(seedBatchID=seedBatch.seedBatchID).first().quantity
        seed_description_list.append(seed_description)
    
    return seed_description_list

def get_plants_assigned(eID):
    plants_id_list = gardenerOfPlant.query.filter_by(eID=eID).all()

    plants_description_list = []
    for plant in plants_id_list:
        plant_description = {}
        plantObject = plantInfo.query.filter_by(pID=plant.pID).first()
        if plantObject.plantStatus == plantStatus.SOLD or plantObject.plantStatus == plantStatus.DEAD:
            continue
        plant_description['date_sown']  = plantObject.dateSown.date()
        plant_description['status']     = plantObject.plantStatus.value
        plant_description['name']       = plantTypeInfo.query.filter_by(plantTypeID=plantObject.plantTypeID).first().plantTypeName
        plant_description['id']         = plant.pID
        plant_description['image']      = plantImages.query.filter_by(plantTypeID=plantObject.plantTypeID).first().imageLink
        plants_description_list.append(plant_description)
    
    return plants_description_list

def get_plant_profile(pID):
    plant = plantInfo.query.filter_by(pID=pID).first()
    description = {}
    description['id']           = pID
    description['seedBatchID'] = plant.seedBatchID
    description['colour']       = plant.plantColour
    description['dateSown']     = str(plant.dateSown.date())
    description['status']       = plant.plantStatus.value
    description['typeID']       = plant.plantTypeID
    cost                        = costToRaise.query.filter_by(pID=pID).first()
    description['cost']         = cost.cost
    plantType                   = plantTypeInfo.query.filter_by(plantTypeID=description['typeID']).first()
    description['name']         = plantType.plantTypeName
    description['image']       = plantImages.query.filter_by(plantTypeID=description['typeID']).first().imageLink
    plantUses                   = plantTypeUses.query.filter_by(plantTypeID=plantType.plantTypeID).first()
    
    description['uses']         = []
    if plantUses.cosmetic       == True:
        description['uses'].append('cosmetic')
    if plantUses.medicinal      == True:
        description['uses'].append('medicinal')
    if plantUses.decorative     == True:
        description['uses'].append('decorative')
    if plantUses.edible         == True:
        description['uses'].append('edible')

    plantDescription            = plantTypeDescription.query.filter_by(plantTypeID=plantType.plantTypeID).first()
    description['fertilizer']   = plantDescription.fertilizer
    description['water']        = plantDescription.waterRequirements
    description['weather']      = plantDescription.weatherCondition.value
    description['sunlight']     = plantDescription.sunlightCondition.value
    description['potSize']      = plantDescription.potSize.value
    description['special']      = plantDescription.specialRequirements

    gardenerID                  = gardenerOfPlant.query.filter_by(pID=pID).first().eID
    gardener                    = User.query.filter_by(id=gardenerID).first()
    description['gardener']     = gardener.name
    description['gardenerID']   = gardenerID

    return description

def get_stats_for_status_comparison(gardnerID):
    plant_ids = gardenerOfPlant.query.filter_by(eID=gardnerID).all()
    grown_plants = []
    growing_plants = []
    sold_plants = []
    dead_plants = []
    index = {'growing':{}, 'grown':{}, 'sold':{}}  # Plant Types

    for plant_id in plant_ids:
        plant = plantInfo.query.filter_by(pID=plant_id.pID).first()
        plantType = plantTypeInfo.query.filter_by(plantTypeID=plant.plantTypeID).first()
        
        try:
            index['growing'][plantType.plantTypeName]
            index['grown'][plantType.plantTypeName]
            index['sold'][plantType.plantTypeName]
        except:
            index['growing'][plantType.plantTypeName] = 0
            index['grown'][plantType.plantTypeName] = 0
            index['sold'][plantType.plantTypeName] = 0
        
    
        if plant.plantStatus == plantStatus.GROWING:
            index['growing'][plantType.plantTypeName] += 1
        elif plant.plantStatus == plantStatus.GROWN:
            index['grown'][plantType.plantTypeName] += 1
        elif plant.plantStatus == plantStatus.SOLD:
            index['sold'][plantType.plantTypeName] += 1

    a = pd.DataFrame(index)
    fig = a.plot.bar(rot=0).get_figure()
    fig.suptitle('Plant Status Distribution', fontsize=18)
    plt.xlabel('Plant Type', fontsize=16)
    plt.ylabel('Numbers', fontsize=16)
    
    DIR = os.path.join(BASE_STATS_DIR, 'plantsStatusComparison')
    Path(DIR).mkdir(parents=True, exist_ok=True)
    IMG_PATH = os.path.join(DIR, '{gardenerID}.png'.format(gardenerID=gardnerID))
    fig.savefig(IMG_PATH)
    
    return IMG_PATH.split('app/')[1]
        
    