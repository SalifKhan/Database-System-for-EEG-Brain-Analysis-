from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Length

class SubjectForm(FlaskForm):
    subject_id = IntegerField('ID', validators=[
        DataRequired(),
        NumberRange(min=0)
    ])
    
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    
    age = IntegerField('Age', validators=[
        DataRequired(),
        NumberRange(min=0, max=120)
    ])
    
    gender = SelectField('Gender', choices=[
        ('', 'Select Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Non-binary', 'Non-binary'),
        ('Other', 'Other'),
        ('Prefer not to say', 'Prefer not to say')
    ], validators=[DataRequired()])
    
    handedness = SelectField('Handedness', choices=[
        ('', 'Select Handedness'),
        ('Right', 'Right'),
        ('Left', 'Left'),
        ('Ambidextrous', 'Ambidextrous')
    ], validators=[DataRequired()])
    
    medical_history = TextAreaField('Medical History')
    
    consent_status = BooleanField('Consent Given') 