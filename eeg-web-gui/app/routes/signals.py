from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import numpy as np
from scipy import signal as sig
from app import db
from app.models import BrainSignal, EEGReading, Subject, CognitiveTask, EEGDevice, Researcher
from app.forms.signal import SignalUploadForm

bp = Blueprint('signals', __name__, url_prefix='/signals')

@bp.route('/', methods=['GET'])
def list():
    signals = BrainSignal.query.all()
    eeg_readings = EEGReading.query.all()
    return render_template('signals/list.html', signals=signals, eeg_readings=eeg_readings)

@bp.route('/', methods=['POST'])
def create():
    try:
        signal = BrainSignal(
            recording_id=request.form['recording_id'],
            channel_name=request.form['channel_name'],
            timestamp=datetime.strptime(request.form['timestamp'], '%Y-%m-%dT%H:%M'),
            amplitude=float(request.form['amplitude']),
            frequency=float(request.form['frequency']) if request.form['frequency'] else None,
            signal_quality=request.form['signal_quality']
        )
        db.session.add(signal)
        db.session.commit()
        flash('Signal added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding signal: {str(e)}', 'danger')
    return redirect(url_for('signals.list'))

@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    form = SignalUploadForm()
    
    # Populate select fields
    form.subject.choices = [(s.subject_id, s.name) for s in Subject.query.all()]
    form.task.choices = [(t.task_id, t.task_name) for t in CognitiveTask.query.all()]
    
    if form.validate_on_submit():
        try:
            filename = None
            if form.signal_file.data:
                # Save the signal file if provided
                file = form.signal_file.data
                filename = secure_filename(file.filename)
                signal_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(signal_path)
            
            # Get the first researcher (temporary solution without login)
            researcher = Researcher.query.first()
            if not researcher:
                flash('No researchers found in the system.', 'danger')
                return redirect(url_for('signals.list'))
            
            # Create EEG Reading record
            reading = EEGReading(
                researcher_id=researcher.researcher_id,
                subject_id=form.subject.data,
                task_id=form.task.data,
                recording_date=datetime.utcnow(),
                equipment_used=filename if filename else 'No file uploaded',
                duration_seconds=form.duration_seconds.data,
                sampling_rate=256,  # Default value
                channel_count=64,   # Default value
                notes=form.notes.data
            )
            db.session.add(reading)
            db.session.flush()  # Get the reading_id
            
            # Create Brain Signal record
            signal = BrainSignal(
                recording_id=reading.recording_id,
                channel_name=form.channel_name.data,
                timestamp=datetime.utcnow(),
                amplitude=0.0,  # Default value
                signal_quality=form.signal_quality.data
            )
            db.session.add(signal)
            db.session.commit()
            
            flash('Signal record created successfully!', 'success')
            return redirect(url_for('signals.list'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating signal record: {str(e)}', 'danger')
            # Log the error for debugging
            current_app.logger.error(f'Signal upload error: {str(e)}')
    
    return render_template('signals/upload.html', form=form)

@bp.route('/<int:signal_id>')
def view(signal_id):
    signal = BrainSignal.query.get_or_404(signal_id)
    return render_template('signals/view.html', signal=signal)

@bp.route('/<int:signal_id>/analyze')
def analyze(signal_id):
    signal = BrainSignal.query.get_or_404(signal_id)
    # Generate sample data for initial display
    sample_data = generate_sample_data()
    return render_template('signals/analyze.html', signal=signal, initial_data=sample_data)

@bp.route('/<int:signal_id>/analyze/data', methods=['POST'])
def analyze_data(signal_id):
    signal = BrainSignal.query.get_or_404(signal_id)
    
    # Get analysis parameters from request
    params = request.get_json()
    analysis_type = params.get('analysisType', 'fft')
    time_start = float(params.get('timeStart', 0))
    time_end = float(params.get('timeEnd', 10))
    freq_min = float(params.get('freqMin', 0))
    freq_max = float(params.get('freqMax', 50))
    
    # Generate sample data (replace with actual signal processing)
    data = process_signal_data(signal, analysis_type, time_start, time_end, freq_min, freq_max)
    
    return jsonify(data)

def generate_sample_data():
    """Generate sample EEG data for initial display"""
    # Time points
    t = np.linspace(0, 10, 1000)
    
    # Generate sample signal with multiple frequency components
    signal = (
        2 * np.sin(2 * np.pi * 10 * t) +  # Alpha wave (10 Hz)
        1 * np.sin(2 * np.pi * 5 * t) +   # Theta wave (5 Hz)
        0.5 * np.sin(2 * np.pi * 20 * t)  # Beta wave (20 Hz)
    )
    
    # Add some noise
    noise = np.random.normal(0, 0.2, len(t))
    signal = signal + noise
    
    return {
        'time': t.tolist(),
        'amplitude': signal.tolist()
    }

def process_signal_data(signal, analysis_type, time_start, time_end, freq_min, freq_max):
    """Process signal data based on analysis type and parameters"""
    # Generate sample time series
    t = np.linspace(time_start, time_end, 1000)
    
    # Generate synthetic signal based on analysis type
    if analysis_type == 'fft':
        # Generate frequency components
        freqs = np.linspace(freq_min, freq_max, 100)
        signal_data = np.zeros_like(t)
        
        # Add frequency components
        for freq in [10, 20, 30]:  # Example frequencies
            if freq_min <= freq <= freq_max:
                signal_data += np.sin(2 * np.pi * freq * t)
        
        # Compute FFT
        fft_freqs = np.fft.fftfreq(len(t), t[1] - t[0])
        fft_data = np.abs(np.fft.fft(signal_data))
        
        # Filter frequencies within range
        mask = (fft_freqs >= freq_min) & (fft_freqs <= freq_max)
        fft_freqs = fft_freqs[mask]
        fft_data = fft_data[mask]
        
        data = {
            'raw': {
                'time': t.tolist(),
                'amplitude': signal_data.tolist()
            },
            'processed': {
                'time': t.tolist(),
                'amplitude': signal_data.tolist()
            },
            'frequency': {
                'freq': fft_freqs.tolist(),
                'power': fft_data.tolist()
            },
            'timefreq': {
                'time': t[::20].tolist(),
                'freq': np.linspace(freq_min, freq_max, 50).tolist(),
                'power': np.random.rand(50, len(t[::20])).tolist()
            },
            'bands': {
                'labels': ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma'],
                'powers': [25, 15, 30, 20, 10]
            }
        }
    else:
        # For other analysis types, generate similar structure with appropriate data
        data = generate_sample_data()
    
    return data

@bp.route('/<int:signal_id>/delete', methods=['POST'])
def delete(signal_id):
    try:
        signal = BrainSignal.query.get_or_404(signal_id)
        db.session.delete(signal)
        db.session.commit()
        flash('Signal deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting signal: {str(e)}', 'danger')
    return redirect(url_for('signals.list')) 