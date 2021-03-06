# Import flask and template operators
from flask import Flask, render_template, session

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy


# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404



# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_landing.controllers import mod_landing as landing_module
from app.mod_customer.controllers import mod_customer as customer_module
from app.mod_owner.controllers import mod_owner as owner_module
from app.mod_manager.controllers import mod_manager as manager_module
from app.mod_gardener.controllers import mod_gardener as gardener_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(landing_module)
app.register_blueprint(customer_module)
app.register_blueprint(owner_module)
app.register_blueprint(manager_module)
app.register_blueprint(gardener_module)

# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy

# Import the userInfo table
from app.mod_auth.models import User
# Import the employeeInfo table
from app.mod_owner.models import employeeInfo
# Import the nurseryInfo table
from app.mod_owner.models import nurseryInfo

db.create_all()
