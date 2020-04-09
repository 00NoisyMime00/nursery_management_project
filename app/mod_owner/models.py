# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

from app.mod_auth.models import User


class employeeInfo(db.Model):
    __tablename__ = 'employeeInfo'
    
    # Employee ID
    eID = db.Column(db.Integer, db.ForeignKey(User.id), primary_key = True)
    # Owner ID
    ownerID = db.Column(db.Integer, db.ForeignKey(User.id), primary_key = True)

    def __init__(self, eID, ownerID):
        
        self.eID        = eID
        self.ownerID    = ownerID

    def __repr__(self):

        return '<Owner {oID} employee-{eID}>'.format(oID = self.ownerID, eID = self.eID) 


class nurseryInfo(db.Model):
    __tablename__ = 'nurseryInfo'

    # Nursery ID
    nID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    # Owner ID
    ownerID = db.Column(db.Integer, db.ForeignKey(User.id), primary_key = True)
    # Maintenance cost
    maintenanceCost = db.Column(db.Numeric(10, 2))
    # Labour cost
    labourCost = db.Column(db.Numeric(10, 2))
    # Not tested
    address = db.relationship("nurseryAddress", backref="nurseryInfo", cascade="all, delete-orphan", lazy='dynamic')
    # Not tested
    staff = db.relationship("nurseryStaff", backref="nurseryInfo", cascade='all, delete-orphan', lazy='dynamic')

    def __init__(self, ownerID, maintenanceCost, labourCost):
        
        self.ownerID            = ownerID
        self.maintenanceCost    = maintenanceCost
        self.labourCost         = labourCost
    
    def __repr__(self):
        
        return '<Nursery ID: {id}>'.format(self.nID)
    
    def get_details(self):
        return (self.nID, self.maintenanceCost, self.labourCost)


class nurseryAddress(db.Model):
    __tablename__ = 'nurseryAddress'

    nID     = db.Column(db.Integer,  db.ForeignKey(nurseryInfo.nID), primary_key=True)
    pincode = db.Column(db.Numeric(10, 0), nullable=False)
    city    = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)

    def __init__(self, nID, pincode, city, country):

        self.nID        = nID
        self.pincode    = pincode
        self.city       = city
        self.country    = country
    
    def __repr__(self):
        return '<Nursery ID-{nID} pincode-{pincode} city-{city}>'.format(nID=self.nID, pincode=self.pincode, city=self.city)
    
    def get_complete_address(self):
        return (self.pincode, self.city, self.country)
    

class nurseryStaff(db.Model):
    __tablename__ = 'nurseryStaff'

    nID = db.Column(db.Integer, db.ForeignKey(nurseryInfo.nID), nullable=False)
    eID = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)

    def __init__(self, nID, eID):

        self.nID = nID
        self.eID = eID
    
    def __repr__(self):
        return '<eID-{eID} nID-{nID}>'.format(eID=self.eID, nID=self.nID)