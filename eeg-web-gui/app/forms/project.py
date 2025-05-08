from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Optional

class ProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[
        DataRequired(),
        Length(min=3, max=100)
    ])
    
    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=1000)
    ])
    
    start_date = DateField('Start Date', validators=[DataRequired()])
    
    end_date = DateField('End Date', validators=[Optional()])
    
    status = SelectField('Status', choices=[
        ('', 'Select Status'),
        ('Active', 'Active'),
        ('On Hold', 'On Hold'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    
    funding_source = StringField('Funding Source', validators=[
        Optional(),
        Length(max=100)
    ])
    
    researchers = SelectMultipleField('Researchers', coerce=int) 