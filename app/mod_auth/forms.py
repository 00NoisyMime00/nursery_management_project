# Import Form and RecaptchaField (optional)
# , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
# BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo
from wtforms import TextField, Form, BooleanField, StringField, PasswordField, validators
from wtforms.fields.core import RadioField, SelectField


# Define the login form (WTForms)

class LoginForm(Form):
    email    = email = StringField('Email Address', [validators.Length(min=6, max=35), validators.DataRequired(),])
    password = PasswordField('New Password', [validators.DataRequired()])

class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25), validators.DataRequired(),])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.DataRequired(),])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password') 
    role = SelectField('Role', choices=[('0','Customer'),('1','Owner')])