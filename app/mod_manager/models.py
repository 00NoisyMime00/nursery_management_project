# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

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