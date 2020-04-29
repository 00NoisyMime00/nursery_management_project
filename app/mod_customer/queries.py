from app import db

from app.mod_gardener.models import plantInfo, plantStatus, plantTypeInfo, plantsAvailable, seedTypeInfo

from app.mod_manager.models import plantImages, plantTypeUses, plantTypesAvailable, plantTypeDescription

from app.mod_customer.models import transactionInfo, plantsSold, cart

def get_plants_available():
    
    plant_ids = plantTypesAvailable.query.filter_by().all()
    plants_list = []
    
    for plant_id in plant_ids:
        plant                       = plantTypeInfo.query.filter_by(plantTypeID=plant_id.plantTypeID).first()
        description                 = {}
        description['id']           = plant.plantTypeID
        description['nID']          = plant.nID
        description['name']         = plant.plantTypeName
        description['sellingPrice'] = plant.sellingPrice
        description['quantity']     = len(plantInfo.query.join(plantTypeInfo, plantInfo.plantTypeID==plantTypeInfo.plantTypeID)\
                                        .join(plantsAvailable, plantInfo.pID==plantsAvailable.pID).all())
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
    description['quantity']     = len(plantInfo.query.join(plantsAvailable, plantInfo.pID==plantsAvailable.pID).all())
    description['colour']       = []
    seedType                    = seedTypeInfo.query.filter_by(plantTypeID=pID).all()
    for seed in seedType:
        if seed.plantColor.lower() not in description['colour']:
            description['colour'].append(seed.plantColor.lower())
    
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

def get_order_history(userID):
    orders = transactionInfo.query.filter_by(customerID=userID).all()
    order_discription = []

    for order in orders:
        plants = plantsSold.query.filter_by(transactionID=order.transactionID).all()
        if plants != []:
            for plant in plants:
                plantTypeID = plantInfo.query.filter_by(pID=plant.pID).first().plantTypeID
                description = get_complete_plant_info(plantTypeID)
                description['id'] = plant.pID
                description['sellingPrice'] = plant.sellingPrice
                description['date']         = plant.dateOfSelling
                order_discription.append(description)

    return order_discription

def get_cart_items(userID):
    items = cart.query.filter_by(customerID=userID).all()
    item_description = []

    for item in items:
        plantTypeID = plantInfo.query.filter_by(pID=item.pID).first().plantTypeID
        description = get_complete_plant_info(plantTypeID)
        description['id'] = item.pID
        item_description.append(description)
    
    return item_description

def get_nursery_for_plant(pID):

    # nID = plantTypeInfo.query.filter_by(pID=pID).join(plantInfo, plantInfo.plantTypeID==plantTypeInfo.plantTypeID).all()
    nID = plantInfo.query.filter_by(pID=pID).join(plantTypeInfo, plantTypeInfo.plantTypeID==plantInfo.plantTypeID)\
                        .add_columns(plantTypeInfo.nID).first().nID
    return nID
