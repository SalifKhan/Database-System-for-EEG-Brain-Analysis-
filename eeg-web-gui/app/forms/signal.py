from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SelectField, TextAreaField, IntegerField, StringField
from wtforms.validators import DataRequired, Optional

class SignalUploadForm(FlaskForm):
    subject = SelectField('Subject', validators=[DataRequired()], coerce=int)
    task = SelectField('Cognitive Task', validators=[DataRequired()], coerce=int)
    duration_seconds = IntegerField('Duration (seconds)', validators=[DataRequired()])
    channel_name = StringField('Channel', validators=[DataRequired()])
    signal_quality = SelectField('Signal Quality', 
        choices=[('Excellent', 'Excellent'), ('Good', 'Good'), ('Poor', 'Poor')],
        validators=[DataRequired()]
    )
    signal_file = FileField('Signal File', validators=[
        FileAllowed(['edf', 'bdf', 'gdf'], 'Only EEG data files are allowed!')
    ])
    notes = TextAreaField('Notes') 