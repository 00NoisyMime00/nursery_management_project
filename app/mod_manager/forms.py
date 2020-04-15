# Import Form validators
from wtforms.validators import Required, Email, EqualTo
from wtforms import TextField, Form, BooleanField, StringField, PasswordField, validators, IntegerField, FloatField
from wtforms.fields.core import RadioField, SelectField,SelectMultipleField

class AddPlantForm(Form):
    pname = StringField(' Plant Name', [validators.Length(min=4, max=25), validators.DataRequired(),])
    fertilizer = StringField('Fertilizer', [validators.Length(min=4, max=25), validators.DataRequired(),])
    weather = SelectField('Weather', choices=[('summer','Summer'),('winter','Winter'),('all_season','All Season')])
    sunlight = SelectField('Sunlight', choices=[('mild','Mild'),('moderate','Moderate'),('extreme','Extreme')])
    potsize = SelectField('Pot Size', choices=[('small','Small'),('medium','Medium'),('large','Large')])
    water =  IntegerField("Water Requirement (in ml)")
    special = TextField('Special Requirements', [validators.Length(min=4, max=100),])
    uses = SelectMultipleField("Uses",choices=[("cosmetic","Cosmetic"),("medicinal","Medicinal"),("decorative","Decorative"),("edible","Edible")])

class AddGardenerForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25), validators.DataRequired(),])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.DataRequired(),])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password') 
