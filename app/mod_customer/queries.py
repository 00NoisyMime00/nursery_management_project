from app import db

from app.mod_gardener.models import plantInfo, plantStatus

def get_plants_available():
    
    plants = plantInfo.query.filter_by(plantStatus=plantStatus.GROWN).all()