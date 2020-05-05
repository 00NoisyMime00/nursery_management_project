from app import db

from app.mod_auth.models import User

from app.mod_manager.models import plantTypeInfo, nurseryInfo

from app.mod_gardener.models import plantInfo

class transactionInfo(db.Model):
    __tablename__ = 'transactionInfo'

    transactionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customerID    = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, customerID):

        self.customerID    = customerID
    
    def __repr__(self):

        return '<transaction-{tid} customer-{cid}>'.format(tid=self.transactionID, cid=self.customerID)

class plantsSold(db.Model):
    __tablename__ = 'plantsSold'

    transactionID = db.Column(db.Integer, db.ForeignKey(transactionInfo.transactionID), primary_key=True)
    pID           = db.Column(db.Integer, db.ForeignKey(plantInfo.pID))
    nID           = db.Column(db.Integer, db.ForeignKey(nurseryInfo.nID))
    dateOfSelling = db.Column(db.DateTime,  default=db.func.current_timestamp())
    sellingPrice  = db.Column(db.Numeric(10, 2), nullable=False)

    def __init__(self, transactionID, pID, nID, sellingPrice):

        self.transactionID = transactionID
        self.pID           = pID
        self.nID           = nID
        self.sellingPrice  = sellingPrice

    def __repr__(self):

        return '<transaction-{tid} pid-{pid} selling price-{cost}>'.format(tid=self.transactionID, pid=self.pID, cost=self.sellingPrice)

class cart(db.Model):
    __tablename__ = 'cart'

    customerID = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    pID        = db.Column(db.Integer, db.ForeignKey(plantInfo.pID), primary_key=True)

    def __init__(self, customerID, pID):

        self.customerID = customerID
        self.pID        = pID

    def __repr__(self):

        return '<customer-{cid} plant-{pid}>'.format(cid=self.customerID, pid=self.pID)


class complaints(db.Model):
    __tablemname__ = 'complaints'

    complaintNumber = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID          = db.Column(db.Integer, db.ForeignKey(User.id))
    pID             = db.Column(db.Integer, db.ForeignKey(plantInfo.pID), primary_key=True)
    nID             = db.Column(db.Integer, db.ForeignKey(nurseryInfo.nID))
    complaintStatus = db.Column(db.Integer, nullable=False, default=0) # 0 - active, 1 - resolved
    date            = db.Column(db.DateTime,  default=db.func.current_timestamp())
    description     = db.Column(db.String(500), nullable=False)

    def __init__(self, userID, pID, nID, description):

        self.userID      = userID
        self.pID         = pID
        self.nID         = nID
        self.description = description

    def __repr__(self):

        return '<complaint id-{cid} plant-{pid} nursery-{nid} description-{d}>'\
                .format(cid=self.complaintNumber, pid=self.pID, nid=self.nID, d=self.description)