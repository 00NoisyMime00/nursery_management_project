# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

import enum

from app.mod_manager.models import plantTypeInfo
from app.mod_owner.models import nurseryInfo

class seedTypeInfo(db.Model):
    __tablename__ = 'seedTypeInfo'

    seedTypeID  = db.Column(db.Integer, primary_key=True)
    plantTypeID = db.Column(db.Integer, db.ForeignKey(plantTypeInfo.plantTypeID), nullable=False)

    def __init__(self, plantTypeID):

        self.plantTypeID = plantTypeID
    
    def __repr__(self):

        return '<Seed Type Id-{id} plant Type ID-{pid}>'.format(id=self.seedTypeID, pid=self.plantTypeID)

class seedBatchInfo(db.Model):
    __tablename__ = 'seedBatchInfo'

    seedBatchID     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seedTypeID      = db.Column(db.Integer, db.ForeignKey(seedTypeInfo.seedTypeID), primary_key=True)
    batchSize       = db.Column(db.Integer, nullable=False)
    dateOfPurchase  = db.Column(db.DateTime, default=db.func.current_timestamp())
    batchCost       = db.Column(db.Numeric(10, 2), nullable=False)

    def __init__(self, seedTypeID, batchSize, batchCost):

        self.seedTypeID = seedTypeID
        self.batchSize  = batchSize
        self.batchCost  = batchCost

    def __repr__(self):

        return '<Batch id-{bid} seed type id-{sid} batch size-{s} cost-{c}>'\
            .format(bid=self.seedBatchID, sid=self.seedTypeID, s=self.batchSize, c=self.batchCost)

class seedAvailable(db.Model):
    __tablename__ = 'seedAvailable'

    seedBatchID     = db.Column(db.Integer, db.ForeignKey(seedBatchInfo.seedBatchID), primary_key=True)
    nID             = db.Column(db.Integer, db.ForeignKey(nurseryInfo.nID), primary_key=True)
    quantity        = db.Column(db.Integer, db.CheckConstraint('quantity >= 0'), nullable=False)

    def __init__(self, seedBatchID, nID, quantity):

        self.seedBatchID    = seedBatchID
        self.nID            = nID
        self.quantity       = quantity
    
    def __repr__(self):

        return '<seed batch id-{id} nid-{nid} quantity-{q}>'.format(id=self.seedBatchID, nid=self.nID, q=self.quantity)

class plantStatus(enum.Enum):

    GROWING         = 0
    GROWN           = 1
    SOLD            = 2
    DEAD            = 3
    NEEDS_ATTENTION = 4

class plantInfo(db.Model):
    __tablename__ = 'plantInfo'

    pID             = db.Column(db.Integer, primary_key=True)
    plantTypeID     = db.Column(db.Integer, db.ForeignKey(plantTypeInfo.plantTypeID), nullable=False)
    seedBatchID     = db.Column(db.Integer, db.ForeignKey(seedBatchInfo.seedBatchID), nullable=False)
    plantColour     = db.Column(db.String(50), nullable=False)
    plantStatus     = db.Column(db.Enum(plantStatus), nullable=False)

    def __init__(self, plantTypeID, seedBatchID, plantColour,  plantStatus):
        
        self.plantTypeID = plantTypeID
        self.seedBatchID = seedBatchID
        self.plantColour = plantColour
        self.plantStatus = 0

    def __repr__(self):

        return '<pid-{pid} type id-{id} color-{color} status-{status} batch-{bid}>'\
            .format(pid=self.pID, id=self.plantTypeID, color=self.plantColour, status=self.plantStatus, bid=self.seedBatchID)

class costToRaise(db.Model):
    __tablename__ = 'costToRaise'

    pID     = db.Column(db.Integer, db.ForeignKey(plantInfo.pID), primary_key=True)
    cost    = db.Column(db.Numeric(10, 2), nullable=False, default=0)

    def __init__(self, pID):

        self.pID = pID
    
    def __repr__(self):
        
        return '<pid-{id} cost-{cost}>'.format(id=self.pID, cost=self.cost)