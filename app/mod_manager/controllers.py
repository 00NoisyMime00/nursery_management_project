# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort

from markupsafe import escape 

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# import checked_logged_in function
from app.mod_auth.controllers import check_logged_in

# Import the database object from the main app module
from app import db

# Import User model for manager and gardener
from app.mod_auth.models import User
# Import employeeInfo model for Manager and gardener
from app.mod_owner.models import employeeInfo, nurseryStaff

from app.mod_manager.models import plantTypeInfo, plantImages, plantTypeDescription, plantTypeUses, plantTypesAvailable,\
                                    employeeRating

from app.mod_gardener.models import seedTypeInfo, seedBatchInfo, seedAvailable, vendorInfo, vendorSeedInfo, plantInfo, plantStatus

from app.mod_manager.queries import get_gardeners, get_vendors, get_stats_for_selling_price, get_stats_for_seed_available,\
                                        get_active_complaints, resolve_complaint

from app.mod_gardener.queries import get_complete_plant_description

# Import module forms
from app.mod_auth.forms import LoginForm

# Import module models (i.e. User)
from app.mod_auth.models import User
# For image upload making directory
from pathlib import Path

import decimal

# For uploading image
from werkzeug.utils import secure_filename

# For creating image paths
import os
# For editing Images
from PIL import Image
from io import BytesIO

# Base directory to store images
from config import BASE_IMG_DIR
from app.mod_manager.forms import AddPlantForm, AddGardenerForm

from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_manager = Blueprint('manager', __name__, url_prefix='/')

@mod_manager.route('/', methods=['GET'])
def index():
    if check_logged_in(session['role']):
        return redirect(url_for('landing.index'))
    else:
        return redirect(url_for('landing.index'))

@mod_manager.route('/add_gardener', methods=['GET', 'POST'])
def add_gardener():
    if check_logged_in(2):

        nID = nurseryStaff.query.filter_by(eID=session['user_id']).first()
        if nID != None:
            nID = nID.nID

        form = AddGardenerForm(request.form)
        if request.method == 'POST' and nID != None:
            username = form.name.data
            emailID = form.email.data
            password = form.password.data
            role = 3
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            elif User.query.filter_by(emailID = emailID
            ).first() is not None:
                error = 'User {} is already registered.'.format(username)
            if error is None:
                temp = User(username, emailID, generate_password_hash(password), role)
                db.session.add(temp)
                db.session.commit()
                db.session.add(employeeInfo(temp.id , int(session['user_id'])))
                db.session.add(nurseryStaff(nID, temp.id))
                db.session.commit()
            return redirect(url_for('manager.index'))
        if nID != None:
            return render_template('manager/add_gardener.html', form = form ,role=str(session['role']), assigned='True')
        return render_template('manager/not_assigned.html', role=str(session['role']))
    return redirect(url_for('landing.index'))

@mod_manager.route('view_gardeners', methods=['GET'])
def view_gardeners():
    if check_logged_in(2):
        nID = nurseryStaff.query.filter_by(eID=session['user_id']).first()
        if nID != None:
            nID = nID.nID
            gardener_list = get_gardeners(nID)
            
            if gardener_list == []:
                gardener_list = [('', '', ''),]
            return render_template("manager/view_gardeners.html", role = str(session['role']), employee_list = gardener_list)
        return render_template('manager/not_assigned.html', role=str(session['role']))
    return redirect(url_for('landing.index'))

# Helper function for uploaded Images
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@mod_manager.route('/add_plant', methods=['GET', 'POST'])
def add_plant():
    if check_logged_in(2):
        nID = nurseryStaff.query.filter_by(eID=session['user_id']).first()
        
        form = AddPlantForm(request.form)
        if request.method == 'POST' and nID != None:
            nID = nID.nID
            plantName = form.pname.data.lower()
            fertilizer = form.fertilizer.data.lower()
            weather = form.weather.data.lower()
            water = int(form.water.data)
            sunlight = form.sunlight.data.lower()
            potsize = form.potsize.data.lower()
            special = form.special.data.lower()
            uses = form.uses.data

            cosmetic    = False
            medicinal   = False
            decorative  = False
            edible      = False

            for use in uses:
                if 'cosmetic' == use:
                    cosmetic = True
                elif 'medicinal' == use:
                    medicinal = True
                elif 'decorative' == use:
                    decorative = True
                elif 'edible' == use:
                    edible = True
            
            if special == None:
                special = 'None'

            if plantTypeInfo.query.filter_by(plantTypeName=plantName, nID=nID).first() is not None:
                return redirect(url_for('landing.index'))

            plant = plantTypeInfo(plantName, nID)
            db.session.add(plant)
            db.session.commit()

            description = plantTypeDescription(plant.plantTypeID, fertilizer, weather, sunlight, water, potsize, special)
            db.session.add(description)
            db.session.commit()

            plantUses = plantTypeUses(plant.plantTypeID, cosmetic, medicinal, decorative, edible)
            db.session.add(plantUses)
            db.session.commit()

            if 'img' not in request.files:
                return redirect(url_for('landing.index'))
            
            file = request.files['img']

            if file.filename == '':
                return redirect(url_for('landing.index'))

            plantType = plantTypeInfo.query.filter_by(plantTypeName=plantName, nID=nID).first()
            
            IMG_DIR = os.path.join(BASE_IMG_DIR, 'plants/{nID}/{typeID}'.format(nID=nID, typeID=plantType.plantTypeID))

            Path(IMG_DIR).mkdir(parents=True, exist_ok=True)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                IMG_PATH = os.path.join(IMG_DIR, plantName+'.'+filename.rsplit('.')[1].lower())
                
                img = Image.open(BytesIO(file.read()))
                img = img.resize((250, 200))
                img.save(IMG_PATH)
                
                IMG_PATH = 'static/'+IMG_PATH.split('static/')[1]
                db.session.add(plantImages(plantType.plantTypeID, IMG_PATH))
                db.session.commit()
            return redirect(url_for('landing.index'))
        
        if nID != None:
            nID = nID.nID
            return render_template('manager/add_plant.html', form=form ,role=str(session['role']), assigned='True')
        return render_template('manager/not_assigned.html', role=str(session['role']))
    return redirect(url_for('landing.index'))

@mod_manager.route('/view_plants', methods=['GET'])
def view_plants():
    if check_logged_in(2):
        nID = nurseryStaff.query.filter_by(eID=session['user_id']).first()

        if nID != None:
            nID = nID.nID
            plant_type_list = plantTypeInfo.query.filter_by(nID=nID).all()
            plant_description_list = []
            for plant in plant_type_list:
                plant_description = get_complete_plant_description(plant.plantTypeID)
                plant_description['vendors_list'] = get_vendors(plant.plantTypeID, nID)
                plant_description_list.append(plant_description)
            return render_template('manager/view_plants.html', role=str(session['role']), plant_type_list=plant_description_list)

        return render_template('manager/not_assigned.html', role=str(session['role']))

    return redirect(url_for('landing.index'))

@mod_manager.route('/buy_seeds', methods=['POST'])
def buy_seeds():
    if check_logged_in(2):
        nID = nurseryStaff.query.filter_by(eID=session['user_id']).first()
        if nID != None:
            nID = nID.nID
            if request.method == 'POST' and 'checkbox' in request.form:
                data = request.form.getlist('checkbox')

                for vendor in data:
                    vendorID = int(vendor.split('_')[0])
                    plantTypeID = int(vendor.split('_')[1])
                    
                    quantity = request.form["quantity"+str(vendorID)]
                    if quantity != '':
                        quantity = int(quantity)
                        seedTypes = seedTypeInfo.query.filter_by(plantTypeID=plantTypeID).all()
                        for seedType in seedTypes:
                            if vendorSeedInfo.query.filter_by(vendorID=vendorID, seedTypeID=seedType.seedTypeID).first() != None:
                                seedBatch = seedBatchInfo(seedType.seedTypeID, quantity, quantity*vendorSeedInfo.query\
                                    .filter_by(vendorID=vendorID, seedTypeID=seedType.seedTypeID).first().seedCost)
                                db.session.add(seedBatch)
                                db.session.commit()

                                db.session.add(seedAvailable(seedBatch.seedBatchID, nID, quantity))
                                db.session.commit()

                return redirect(url_for('landing.index'))
        return render_template('manager/not_assigned.html', role=str(session['role']))
    return redirect(url_for('landing.index'))

@mod_manager.route('/add_vendor', methods=['GET', 'POST'])
def add_vendor():
    if check_logged_in(2):
        nID = nurseryStaff.query.filter_by(eID=session['user_id']).first()
        if nID != None:
            nID = nID.nID
            if request.method == 'POST':
                plants_sold_id = request.form.getlist('checkbox')

                vendor = vendorInfo(request.form['name'], nID)
                db.session.add(vendor)
                db.session.commit()
                for plant_id in plants_sold_id:
                    cost = request.form[plant_id]
                    if cost != '':
                        cost = int(cost)
        
                        seed_type = seedTypeInfo(int(plant_id))
                        db.session.add(seed_type)
                        db.session.commit()

                        db.session.add(vendorSeedInfo(seed_type.seedTypeID, vendor.vendorID, cost))
                        db.session.commit()

                return redirect(url_for('landing.index'))

            plant_type_list = plantTypeInfo.query.filter_by(nID=nID).all()
            plant_description_list = []
            for plant in plant_type_list:
                plant_description = get_complete_plant_description(plant.plantTypeID)
                plant_description_list.append(plant_description)
            return render_template('manager/add_vendor.html', role=str(session['role']), plant_type_list=plant_description_list)
        return render_template('manager/not_assigned.html', role=str(session['role']))
    return redirect(url_for('landing.index'))

@mod_manager.route('/update_selling_price', methods=['GET', 'POST'])
def update_selling_price():
    if check_logged_in(2) and 'id' in request.args:
       
        nID = nurseryStaff.query.filter_by(eID=session['user_id']).first()
        if nID != None:
            nID = nID.nID
            
            plantTypeID = int(request.args.get('id'))
            if request.method == 'POST':
                plantType  = plantTypeInfo.query.filter_by(plantTypeID=plantTypeID).first()
                sellingPrice = decimal.Decimal(request.form.get('sellingPrice'))

                plantType.sellingPrice = sellingPrice
                # Make it available
                is_available = plantTypesAvailable.query.filter_by(plantTypeID=plantType.plantTypeID).first()
                if not is_available:
                    db.session.add(plantTypesAvailable(plantType.plantTypeID, nID))
                db.session.commit()
                return redirect(url_for('manager.view_plants'))
            IMG_PATH = get_stats_for_selling_price(plantTypeID)
            return render_template('manager/update_selling_price.html', plantTypeID=plantTypeID, role=str(session['role']), IMG_PATH=IMG_PATH)
    
    return redirect(url_for('landing.index'))

@mod_manager.route('/view_stats_manager', methods=['GET'])
def view_stats():
    if check_logged_in(2):
        nID = nurseryStaff.query.filter_by(eID=session['user_id']).first()
        if nID != None:
            nID = nID.nID

            img_seed_available = get_stats_for_seed_available(nID)
            return render_template('manager/stats.html', role=str(session['role']), img_seed_available=img_seed_available)
    
    return redirect(url_for('landing.index'))

@mod_manager.route('/rate_gardener', methods=['POST'])
def rate_gardener():
    if check_logged_in(2):
        nID = nurseryStaff.query.filter_by(eID=session['user_id']).first()
        if nID != None:
            nID = nID.nID

            emailID = request.form.get('emailID')
            score = int(request.form.get('score'))
            employee = User.query.filter_by(emailID=emailID).first()
            rating_column = employeeRating.query.filter_by(eID=employee.id).all()
            if rating_column == []:
                db.session.add(employeeRating(employee.id, score))
                db.session.commit()
            else:
                for rating in rating_column:
                    if rating.date.month == datetime.now().month:
                        rating.score = score
                        db.session.commit()
                        return redirect(url_for('landing.index'))
                
                db.session.add(employeeRating(employee.id, score))
                db.session.commit()
    
    return redirect(url_for('landing.index'))

@mod_manager.route('/view_active_complaints', methods=['GET', 'POST'])
def view_active_complaints():
    if check_logged_in(2):
        nID = nurseryStaff.query.filter_by(eID=session['user_id']).first()
        if nID != None:
            nID = nID.nID

            if request.method == 'POST':
                complaintNumber = int(request.form.get('complaintNumber'))
                active_complaint = resolve_complaint(complaintNumber)
                
            active_complaints = get_active_complaints(nID)
            return render_template('manager/view_active_complaints.html', role=str(session['role']), complaints=active_complaints)
    return redirect(url_for('landing.index'))


