from app import create_app, db
from app.models import (
    Researcher, Subject, CognitiveTask, EEGDevice,
    MLModel, ResearchProject, UserRole, UserAccount
)
from datetime import datetime, date
from werkzeug.security import generate_password_hash

def init_db():
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create test researcher
        researcher = Researcher(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            institution='Test University',
            department='Neuroscience',
            specialization='EEG Analysis'
        )
        db.session.add(researcher)
        db.session.flush()
        
        # Create user roles
        admin_role = UserRole(
            role_name='Admin',
            permissions='all'
        )
        researcher_role = UserRole(
            role_name='Researcher',
            permissions='view,edit,upload'
        )
        db.session.add_all([admin_role, researcher_role])
        db.session.flush()
        
        # Create test user accounts
        admin_user = UserAccount(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            role=admin_role
        )
        researcher_user = UserAccount(
            username='researcher',
            password_hash=generate_password_hash('password123'),
            role=researcher_role,
            researcher=researcher
        )
        db.session.add_all([admin_user, researcher_user])
        
        # Create test subjects
        subjects = [
            Subject(name='Test Subject 1', age=25, gender='Male', handedness='Right', consent_status=True),
            Subject(name='Test Subject 2', age=30, gender='Female', handedness='Left', consent_status=True)
        ]
        db.session.add_all(subjects)
        
        # Create test cognitive tasks
        tasks = [
            CognitiveTask(
                task_name='N-back Test',
                description='Working memory assessment task',
                difficulty_level='Medium',
                duration_seconds=300,
                instructions='Press button when current stimulus matches one presented n trials ago'
            ),
            CognitiveTask(
                task_name='Stroop Test',
                description='Measures reaction time and selective attention',
                difficulty_level='Easy',
                duration_seconds=180,
                instructions='Name the color of the word, not the word itself'
            )
        ]
        db.session.add_all(tasks)
        
        # Create test EEG devices
        devices = [
            EEGDevice(
                manufacturer='BrainScope',
                model='EEG-2000',
                serial_number='BS2000-001',
                specifications='64 channels, 256Hz sampling rate',
                calibration_date=date.today(),
                status='Active'
            ),
            EEGDevice(
                manufacturer='NeuroScan',
                model='Ultra',
                serial_number='NS-U-002',
                specifications='128 channels, 512Hz sampling rate',
                calibration_date=date.today(),
                status='Active'
            )
        ]
        db.session.add_all(devices)
        
        # Create test ML models
        models = [
            MLModel(
                model_name='CNNBrainNet',
                model_type='Convolutional Neural Network',
                framework='TensorFlow',
                accuracy=87.50,
                parameters='Layers: 5, Neurons: 256, Dropout: 0.2',
                creation_date=date.today()
            ),
            MLModel(
                model_name='EEG-LSTM',
                model_type='Long Short-Term Memory Network',
                framework='PyTorch',
                accuracy=92.30,
                parameters='Units: 128, Timesteps: 50',
                creation_date=date.today()
            )
        ]
        db.session.add_all(models)
        
        # Create test research project
        project = ResearchProject(
            project_name='EEG Pattern Analysis',
            description='Investigating neural patterns during cognitive tasks',
            start_date=date.today(),
            status='Active',
            funding_source='Research Grant'
        )
        project.researchers.append(researcher)
        db.session.add(project)
        
        # Commit all changes
        db.session.commit()
        print("Database initialized with test data!")

if __name__ == '__main__':
    init_db() 