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