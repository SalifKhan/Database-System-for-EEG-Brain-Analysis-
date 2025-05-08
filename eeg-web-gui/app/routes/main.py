from flask import Blueprint, render_template, redirect, url_for
from app.models import BrainSignal, ResearchProject

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return redirect(url_for('main.dashboard'))

@bp.route('/dashboard')
def dashboard():
    # Get 5 most recent signals
    recent_signals = BrainSignal.query.order_by(BrainSignal.timestamp.desc()).limit(5).all()
    
    # Get active projects
    active_projects = ResearchProject.query.filter_by(status='Active').order_by(ResearchProject.start_date.desc()).limit(5).all()
    
    return render_template('main/dashboard.html',
                         recent_signals=recent_signals,
                         active_projects=active_projects) 