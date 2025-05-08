from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models import Subject
from app.forms.subject import SubjectForm
import traceback

bp = Blueprint('subjects', __name__, url_prefix='/subjects')

@bp.route('/')
def list():
    subjects = Subject.query.all()
    return render_template('subjects/list.html', subjects=subjects)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    form = SubjectForm()
    if form.validate_on_submit():
        try:
            subject = Subject(
                subject_id=form.subject_id.data,
                name=form.name.data,
                age=form.age.data,
                gender=form.gender.data,
                handedness=form.handedness.data,
                medical_history=form.medical_history.data,
                consent_status=form.consent_status.data
            )
            db.session.add(subject)
            db.session.commit()
            flash('Subject added successfully!', 'success')
            return redirect(url_for('subjects.list'))
        except Exception as e:
            db.session.rollback()
            error_msg = str(e)
            stack_trace = traceback.format_exc()
            print(f"Error adding subject: {error_msg}")
            print(f"Stack trace: {stack_trace}")
            flash(f'Error adding subject: {error_msg}', 'danger')
    elif request.method == 'POST':
        print(f"Form validation errors: {form.errors}")
        flash('Please check the form for errors.', 'danger')
    return render_template('subjects/form.html', form=form)

@bp.route('/<int:subject_id>')
def view(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    return render_template('subjects/view.html', subject=subject)

@bp.route('/<int:subject_id>/edit', methods=['GET', 'POST'])
def edit(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    form = SubjectForm(obj=subject)
    
    if form.validate_on_submit():
        subject.name = form.name.data
        subject.age = form.age.data
        subject.gender = form.gender.data
        subject.handedness = form.handedness.data
        subject.medical_history = form.medical_history.data
        subject.consent_status = form.consent_status.data
        
        try:
            db.session.commit()
            flash('Subject updated successfully!', 'success')
            return redirect(url_for('subjects.list'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating subject. Please try again.', 'danger')
    
    return render_template('subjects/form.html', form=form, subject=subject)

@bp.route('/<int:subject_id>/delete', methods=['POST'])
def delete(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    try:
        db.session.delete(subject)
        db.session.commit()
        flash('Subject deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting subject. Please try again.', 'danger')
    return redirect(url_for('subjects.list')) 