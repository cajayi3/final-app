from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields import SelectMultipleField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    name = StringField('Name', validators= [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    submit_button = SubmitField()

class UserSignupForm(FlaskForm):
    first_name = StringField('First name', validators= [DataRequired()])
    last_name = StringField('Last name', validators= [DataRequired()])
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators= [DataRequired()])
    country = SelectMultipleField('Country', choices = [('australia', 'Australia'), ('canada', 'Canada'), 
    ('united states', 'United States'), ('russia', 'Russia'),('south africa', 'South Africa'), 
    ('england', 'England'), ('france', 'France'), ('mexico', 'Mexico'), ('germany', 'Germany'), 
    ('dominican republic', 'Dominican Republic')])
    submit_button = SubmitField()