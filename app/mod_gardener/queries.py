from app import db

from app.mod_manager.models import plantTypeInfo, plantImages, plantTypeUses

from app.mod_gardener.models import seedTypeInfo, seedBatchInfo, seedAvailable

def get_complete_plant_description(pID):
    description = {}
    
    plant = plantTypeInfo.query.filter_by(plantTypeID=pID).first()
    description['id']       = pID
    description['name']     = plant.plantTypeName
    description['image']    = plantImages.query.filter_by(plantTypeID=plant.plantTypeID).first().imageLink
    
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