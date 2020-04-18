# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

import enum

from app.mod_owner.models import nurseryInfo

class plantTypeInfo(db.Model):
    __tablename__ = 'plantTypeInfo'

    plantTypeID     = db.Column(db.Integer, primary_key=True, autoincrement = True)
    plantTypeName   = db.Column(db.String(100))
    nID             = db.Column(db.Integer, db.ForeignKey(nurseryInfo.nID))
    imageURLS       = db.relationship("plantImages", backref="plantTypeInfo", cascade="all, delete-orphan", lazy='dynamic')

    def __init__(self, plantTypeName, nID):
        
        self.plantTypeName    = plantTypeName
        self.nID            = nID
    
    def __repr__(self):

        return '<Plant Type: {name} id-{id}> nursery-{nID}'.format(name=self.plantTypeName, id=self.plantTypeID, nID=self.nID)

class plantImages(db.Model):
    __tablename__ = 'plantImages'

    imageID         = db.Column(db.Integer, primary_key=True)
    plantTypeID     = db.Column(db.Integer, db.ForeignKey(plantTypeInfo.plantTypeID))
    imageLink       = db.Column(db.String(500), nullable=False)

    def __init__(self, plantTypeID, imageLink):

        self.plantTypeID    = plantTypeID
        self.imageLink      = imageLink

    def __repr__(self):

        return '<Plant Image: location:{location}>'.format(location=self.imageLink)

class weatherConditionTypes(enum.Enum):
    
    SUMMER      = 'summer'
    WINTER      = 'winter'
    ALL_SEASON  = 'all_season'

class sunlightTypes(enum.Enum):

    MILD        = 'mild'
    MODERATE    = 'moderate'
    EXTREME     = 'extreme'

class potSizeTypes(enum.Enum):

    SMALL   = 'small'
    MEDIUM  = 'medium'
    LARGE   = 'large'

class plantTypeDescription(db.Model):
    __tablename__ = 'plantTypeDescription'

    plantTypeID             = db.Column(db.Integer, db.ForeignKey(plantTypeInfo.plantTypeID), primary_key=True)
    fertilizer              = db.Column(db.String(100), nullable=False)
    weatherCondition        = db.Column(db.Enum(weatherConditionTypes), nullable=False)
    sunlightCondition       = db.Column(db.Enum(sunlightTypes), nullable=False)
    waterRequirements       = db.Column(db.Integer, nullable=False)
    potSize                 = db.Column(db.Enum(potSizeTypes), nullable=False)
    specialRequirements     = db.Column(db.String(100), nullable=True)

    def __init__(self, plantTyepID, fertilizer, weatherCondition, sunlightCondition, waterRequirements, potSize, specialRequirements=None):
        
        self.plantTypeID            = plantTyepID
        self.fertilizer             = fertilizer
        self.weatherCondition       = weatherCondition
        self.sunlightCondition      = sunlightCondition
        self.waterRequirements      = waterRequirements
        self.potSize                = potSize
        self.specialRequirements    = specialRequirements

    def __repr__(self):
        
        return '<ID-{id} fertilizer-{fert} weather-{wea} sunlight-{sun} water-{water} pot-{pot} special-{spec}>'\
            .format(id=self.plantTypeID,fert=self.fertilizer, wea=self.weatherCondition, sun=self.sunlightCondition, water=self.waterRequirements, pot=self.potSize, spec=self.specialRequirements)

class plantTypeUses(db.Model):
    __tablename__ = 'plantTypeUses'

    plantTypeID = db.Column(db.Integer, db.ForeignKey(plantTypeInfo.plantTypeID), primary_key=True)
    cosmetic    = db.Column(db.Boolean, nullable=False, default=False)
    medicinal   = db.Column(db.Boolean, nullable=False, default=False)
    decorative  = db.Column(db.Boolean, nullable=False, default=False)
    edible      = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, plantTyepID, cosmetic=False, medicinal=False, decorative=False, edible=False):

        self.plantTypeID    = plantTyepID
        self.cosmetic       = cosmetic
        self.medicinal      = medicinal
        self.decorative     = decorative
        self.edible         = edible

    def __repr__(self):

        return '<id-{id} cosmetic-{c} medicinal-{m} decorative-{d} edible-{e}>'\
            .format(id=self.plantTypeID, c=self.cosmetic, m=self.medicinal, d=self.decorative, e=self.edible)