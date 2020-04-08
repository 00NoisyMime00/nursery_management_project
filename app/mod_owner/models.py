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