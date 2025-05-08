from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField
from wtforms.validators import DataRequired, Email, Length

class ResearcherForm(FlaskForm):
    researcher_id = IntegerField('ID', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    email = EmailField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=100)
    ])
    institution = StringField('Institution', validators=[
        Length(max=100)
    ])
    department = StringField('Department', validators=[
        Length(max=100)
    ])
    specialization = StringField('Specialization', validators=[
        Length(max=100)
    ]) 