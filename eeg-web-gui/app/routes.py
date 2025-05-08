from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Researcher, Subject, BrainSignal, ResearchProject, EEGReading

main = Blueprint('main', __name__)

@main.route('/')
def index():
    subject_count = Subject.query.count()
    project_count = ResearchProject.query.count()
    signal_count = BrainSignal.query.count()
    researcher_count = Researcher.query.count()
    # Recent activity: last 5 subjects, signals, and projects
    recent_subjects = Subject.query.order_by(Subject.created_at.desc()).limit(2).all()
    recent_signals = BrainSignal.query.order_by(BrainSignal.created_at.desc()).limit(2).all()
    recent_projects = ResearchProject.query.order_by(ResearchProject.created_at.desc()).limit(1).all()
    recent_activities = []
    for s in recent_subjects:
        recent_activities.append({'description': f"New subject added: {s.name} (ID: {s.subject_id})"})
    for sig in recent_signals:
        recent_activities.append({'description': f"New signal added for Recording ID: {sig.recording_id}"})
    for p in recent_projects:
        recent_activities.append({'description': f"New project created: {p.project_name}"})
    return render_template('index.html', 
        subject_count=subject_count, 
        project_count=project_count, 
        signal_count=signal_count, 
        researcher_count=researcher_count, 
        recent_activities=recent_activities
    )

@main.route('/researchers')
def researchers():
    researchers = Researcher.query.all()
    return render_template('researchers.html', researchers=researchers)

@main.route('/add_researcher', methods=['POST'])
def add_researcher():
    try:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        institution = request.form.get('institution')
        department = request.form.get('department')
        specialization = request.form.get('specialization')

        if not all([first_name, last_name, email]):
            # Flash an error message here if you have Flask flash messaging set up
            return redirect(url_for('main.researchers'))

        new_researcher = Researcher(
            first_name=first_name,
            last_name=last_name,
            email=email,
            institution=institution,
            department=department,
            specialization=specialization
        )
        db.session.add(new_researcher)
        db.session.commit()
    except Exception as e:
        # Log the error here if you have logging set up
        print(f"Error adding researcher: {str(e)}")
        db.session.rollback()
    return redirect(url_for('main.researchers'))

subjects = Blueprint('subjects', __name__, url_prefix='/subjects')
@subjects.route('/', methods=['GET', 'POST'])
def list_subjects():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        new_subject = Subject(name=name, age=age, gender=gender)
        db.session.add(new_subject)
        db.session.commit()
        return redirect(url_for('subjects.list_subjects'))
    subjects = Subject.query.all()
    return render_template('subjects.html', subjects=subjects)

signals = Blueprint('signals', __name__, url_prefix='/signals')
@signals.route('/', methods=['GET', 'POST'])
def list_signals():
    if request.method == 'POST':
        recording_id = request.form['recording_id']
        channel_name = request.form['channel_name']
        timestamp = request.form['timestamp']
        amplitude = request.form['amplitude']
        frequency = request.form.get('frequency')
        signal_quality = request.form.get('signal_quality')
        new_signal = BrainSignal(
            recording_id=recording_id,
            channel_name=channel_name,
            timestamp=timestamp,
            amplitude=amplitude,
            frequency=frequency,
            signal_quality=signal_quality
        )
        db.session.add(new_signal)
        db.session.commit()
        return redirect(url_for('signals.list_signals'))
    signals = BrainSignal.query.all()
    eeg_readings = EEGReading.query.all()
    return render_template('signals.html', signals=signals, eeg_readings=eeg_readings)

projects = Blueprint('projects', __name__, url_prefix='/projects')
@projects.route('/', methods=['GET', 'POST'])
def list_projects():
    if request.method == 'POST':
        project_name = request.form['name']
        description = request.form['description']
        # You may want to add start_date, end_date, status, funding_source as well
        new_project = ResearchProject(project_name=project_name, description=description, start_date=None)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('projects.list_projects'))
    projects = ResearchProject.query.all()
    return render_template('projects.html', projects=projects) 