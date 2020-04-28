from app import db

from app.mod_gardener.models import plantInfo, plantStatus, plantTypeInfo, plantsAvailable, seedTypeInfo

from app.mod_manager.models import plantImages, plantTypeUses, plantTypesAvailable, plantTypeDescription

def get_plants_available():
    
    plant_ids = plantTypesAvailable.query.filter_by().all()
    plants_list = []
    
    for plant_id in plant_ids:
        plant                       = plantTypeInfo.query.filter_by(plantTypeID=plant_id.plantTypeID).first()
        description                 = {}
        description['id']           = plant.plantTypeID
        description['nID']          = plant.nID
        description['name']         = plant.plantTypeName
        description['colour']       = seedTypeInfo.query.filter_by(plantTypeID=plant_id.plantTypeID).first().plantColor
        description['sellingPrice'] = plant.sellingPrice
        description['quantity']     = len(plantInfo.query.filter_by(plantTypeID=plant_id.plantTypeID, plantStatus=plantStatus.GROWN).all())
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
        
        plants_list.append(description)
    
    return plants_list

def get_complete_plant_info(pID):
    description = {}
    plant = plantTypeInfo.query.filter_by(plantTypeID=pID).first()
    description['id']           = plant.plantTypeID
    description['nID']          = plant.nID
    description['name']         = plant.plantTypeName
    description['sellingPrice'] = plant.sellingPrice
    description['colour']       = seedTypeInfo.query.filter_by(plantTypeID=pID).first().plantColor
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

    plantDescription            = plantTypeDescription.query.filter_by(plantTypeID=pID).first()
    description['fertilizer']   = plantDescription.fertilizer
    description['water']        = plantDescription.waterRequirements
    description['weather']      = plantDescription.weatherCondition.value
    description['sunlight']     = plantDescription.sunlightCondition.value
    description['potSize']      = plantDescription.potSize.value
    description['special']      = plantDescription.specialRequirements
    
    return description