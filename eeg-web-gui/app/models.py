from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

# Association table for many-to-many relationship between Research_Project and Researcher
project_researcher = db.Table('Project_Researcher',
    db.Column('project_id', db.Integer, db.ForeignKey('Research_Project.project_id'), primary_key=True),
    db.Column('researcher_id', db.Integer, db.ForeignKey('Researcher.researcher_id'), primary_key=True),
    db.Column('role', db.String(50), nullable=False),
    db.Column('start_date', db.Date, nullable=False),
    db.Column('end_date', db.Date),
    db.Column('created_at', db.TIMESTAMP, server_default=db.func.current_timestamp())
)

class Researcher(db.Model):
    __tablename__ = 'Researcher'
    researcher_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    institution = db.Column(db.String(100))
    department = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # Relationships
    eeg_readings = db.relationship('EEGReading', backref='researcher', lazy=True)
    projects = db.relationship('ResearchProject', secondary=project_researcher, backref=db.backref('researchers', lazy=True))

    def __repr__(self):
        return f"<Researcher {self.first_name} {self.last_name}>"

class Subject(db.Model):
    __tablename__ = 'Subject'
    subject_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20))
    handedness = db.Column(db.String(20))
    medical_history = db.Column(db.Text)
    consent_status = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # Relationships
    eeg_readings = db.relationship('EEGReading', backref='subject', lazy=True)

    def __repr__(self):
        return f"<Subject {self.name}>"

class CognitiveTask(db.Model):
    __tablename__ = 'Cognitive_Task'
    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    difficulty_level = db.Column(db.String(50))
    duration_seconds = db.Column(db.Integer)
    instructions = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # Relationships
    eeg_readings = db.relationship('EEGReading', backref='task', lazy=True)

    def __repr__(self):
        return f"<CognitiveTask {self.task_name}>"

class EEGDevice(db.Model):
    __tablename__ = 'EEG_Device'
    device_id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(50), unique=True)
    specifications = db.Column(db.Text)
    calibration_date = db.Column(db.Date)
    last_maintenance_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='Active')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f"<EEGDevice {self.manufacturer} {self.model}>"

class EEGReading(db.Model):
    __tablename__ = 'EEG_Reading'
    recording_id = db.Column(db.Integer, primary_key=True)
    researcher_id = db.Column(db.Integer, db.ForeignKey('Researcher.researcher_id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('Subject.subject_id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('Cognitive_Task.task_id'), nullable=False)
    recording_date = db.Column(db.TIMESTAMP, nullable=False)
    duration_seconds = db.Column(db.Integer)
    equipment_used = db.Column(db.String(100))
    sampling_rate = db.Column(db.Integer)
    channel_count = db.Column(db.Integer)
    notes = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # Relationships
    brain_signals = db.relationship('BrainSignal', backref='eeg_reading', lazy=True, cascade='all, delete-orphan')
    experiment_logs = db.relationship('ExperimentLog', backref='eeg_reading', lazy=True)

    def __repr__(self):
        return f"<EEGReading {self.recording_id}>"

class BrainSignal(db.Model):
    __tablename__ = 'Brain_Signal'
    signal_id = db.Column(db.Integer, primary_key=True)
    recording_id = db.Column(db.Integer, db.ForeignKey('EEG_Reading.recording_id'), nullable=False)
    channel_name = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    amplitude = db.Column(db.Numeric(10,6), nullable=False)
    frequency = db.Column(db.Numeric(10,2))
    signal_quality = db.Column(db.String(20))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # Relationships
    analyses = db.relationship('SignalAnalysis', backref='brain_signal', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<BrainSignal {self.signal_id}>"

class MLModel(db.Model):
    __tablename__ = 'ML_Model'
    model_id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100), nullable=False)
    model_type = db.Column(db.String(50))
    framework = db.Column(db.String(50))
    accuracy = db.Column(db.Numeric(5,2))
    parameters = db.Column(db.Text)
    creation_date = db.Column(db.Date)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f"<MLModel {self.model_name}>"

class SignalAnalysis(db.Model):
    __tablename__ = 'Signal_Analysis'
    analysis_id = db.Column(db.Integer, primary_key=True)
    signal_id = db.Column(db.Integer, db.ForeignKey('Brain_Signal.signal_id'), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('ML_Model.model_id'), nullable=False)
    analysis_type = db.Column(db.String(50), nullable=False)
    analysis_date = db.Column(db.TIMESTAMP, nullable=False)
    features = db.Column(db.Text)
    results = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # Relationships
    ml_model = db.relationship('MLModel', backref='analyses', lazy=True)

    def __repr__(self):
        return f"<SignalAnalysis {self.analysis_id}>"

class ResearchProject(db.Model):
    __tablename__ = 'Research_Project'
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='Active')
    funding_source = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f"<ResearchProject {self.project_name}>"

class ExperimentLog(db.Model):
    __tablename__ = 'Experiment_Log'
    log_id = db.Column(db.Integer, primary_key=True)
    recording_id = db.Column(db.Integer, db.ForeignKey('EEG_Reading.recording_id'))
    event_type = db.Column(db.String(50))
    event_time = db.Column(db.TIMESTAMP)
    description = db.Column(db.Text)
    severity = db.Column(db.String(20))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp()) 