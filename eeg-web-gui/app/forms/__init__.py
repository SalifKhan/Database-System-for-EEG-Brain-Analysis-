from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField, TextAreaField, DateField, IntegerField, DecimalField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Sign Up')

class ResearcherForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    institution = StringField('Institution')
    department = StringField('Department')
    specialization = StringField('Specialization')

class SubjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    handedness = SelectField('Handedness', choices=[('right', 'Right'), ('left', 'Left'), ('ambidextrous', 'Ambidextrous')])
    medical_history = TextAreaField('Medical History')
    consent_status = BooleanField('Consent Given')

class EEGReadingForm(FlaskForm):
    researcher_id = SelectField('Researcher', coerce=int)
    subject_id = SelectField('Subject', coerce=int)
    task_id = SelectField('Task', coerce=int)
    device_id = SelectField('Device', coerce=int)
    recording_date = DateField('Recording Date', validators=[DataRequired()])
    duration_seconds = IntegerField('Duration (seconds)')
    equipment_used = StringField('Equipment Used')
    sampling_rate = IntegerField('Sampling Rate')
    channel_count = IntegerField('Channel Count')
    notes = TextAreaField('Notes')

class BrainSignalForm(FlaskForm):
    recording_id = SelectField('Recording', coerce=int)
    channel_name = StringField('Channel Name', validators=[DataRequired()])
    amplitude = DecimalField('Amplitude', validators=[DataRequired()])
    frequency = DecimalField('Frequency')
    signal_quality = SelectField('Signal Quality', choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    ])

class ProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[Optional()])
    status = SelectField('Status', choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled')
    ])
    funding_source = StringField('Funding Source')

class DeviceForm(FlaskForm):
    manufacturer = StringField('Manufacturer', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    serial_number = StringField('Serial Number', validators=[DataRequired()])
    specifications = TextAreaField('Specifications')
    calibration_date = DateField('Calibration Date')
    last_maintenance_date = DateField('Last Maintenance Date')
    status = SelectField('Status', choices=[
        ('active', 'Active'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired')
    ])

class PublicationForm(FlaskForm):
    project_id = SelectField('Project', coerce=int)
    title = StringField('Title', validators=[DataRequired()])
    authors = TextAreaField('Authors', validators=[DataRequired()])
    publication_date = DateField('Publication Date')
    journal = StringField('Journal')
    doi = StringField('DOI') 