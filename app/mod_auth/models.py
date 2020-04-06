# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    dateOfJoining  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

# Define a User model
class User(Base):

    __tablename__ = 'userInfo'

    # User Name
    name    = db.Column(db.String(100),  nullable=False)

    # Identification Data: email & password
    emailID    = db.Column(db.String(100),  nullable=False,
                                            unique=True)
    password = db.Column(db.String(200),  nullable=False)

    # Authorisation Data: role & status
    role     = db.Column(db.SmallInteger, nullable=False)   # 0 - customer, 1 - Owner, 2 - Manager, 3 - Gardener
    # status   = db.Column(db.SmallInteger, nullable=False)   # yet to be decided

    # New instance instantiation procedure
    def __init__(self, name, email, password, role):

        self.name     = name
        self.emailID   = email
        self.password = password
        self.role = role

    def __repr__(self):
        return '<User {name} id-{id}>'.format(name = self.name, id = self.id)                        
