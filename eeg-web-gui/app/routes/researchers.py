from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models import Researcher
from app.forms.researcher import ResearcherForm
import traceback

bp = Blueprint('researchers', __name__, url_prefix='/researchers')

@bp.route('/')
def list():
    researchers = Researcher.query.all()
    return render_template('researchers/list.html', researchers=researchers)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    form = ResearcherForm()
    if form.validate_on_submit():
        try:
            researcher = Researcher(
                researcher_id=form.researcher_id.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                institution=form.institution.data,
                department=form.department.data,
                specialization=form.specialization.data
            )
            db.session.add(researcher)
            db.session.commit()
            flash('Researcher added successfully!', 'success')
            return redirect(url_for('researchers.list'))
        except Exception as e:
            db.session.rollback()
            error_msg = str(e)
            print(f"Error adding researcher: {error_msg}")
            print(f"Stack trace: {traceback.format_exc()}")
            flash(f'Error adding researcher: {error_msg}', 'danger')
    return render_template('researchers/form.html', form=form)

@bp.route('/<int:researcher_id>')
def view(researcher_id):
    researcher = Researcher.query.get_or_404(researcher_id)
    return render_template('researchers/view.html', researcher=researcher)

@bp.route('/<int:researcher_id>/edit', methods=['GET', 'POST'])
def edit(researcher_id):
    researcher = Researcher.query.get_or_404(researcher_id)
    form = ResearcherForm(obj=researcher)
    
    if form.validate_on_submit():
        try:
            researcher.first_name = form.first_name.data
            researcher.last_name = form.last_name.data
            researcher.email = form.email.data
            researcher.institution = form.institution.data
            researcher.department = form.department.data
            researcher.specialization = form.specialization.data
            
            db.session.commit()
            flash('Researcher updated successfully!', 'success')
            return redirect(url_for('researchers.list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating researcher: {str(e)}', 'danger')
    
    return render_template('researchers/form.html', form=form, researcher=researcher)

@bp.route('/<int:researcher_id>/delete', methods=['POST'])
def delete(researcher_id):
    researcher = Researcher.query.get_or_404(researcher_id)
    try:
        db.session.delete(researcher)
        db.session.commit()
        flash('Researcher deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting researcher: {str(e)}', 'danger')
    return redirect(url_for('researchers.list')) 