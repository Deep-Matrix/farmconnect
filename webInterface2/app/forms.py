from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = IntegerField('Username', validators=[DataRequired()])
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