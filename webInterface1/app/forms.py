from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    phonenum = IntegerField('Phone Number', validators=[DataRequired()])
    fullname = StringField('Full Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    aadhar = IntegerField('Aadhar Details', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class AddProduceForm(FlaskForm):
    producename = StringField('Producename', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    cost = IntegerField('cost', validators=[DataRequired()])
    sold = BooleanField('sold', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    submit = SubmitField('Add Produce')