from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from app.models import ResearchProject, Researcher
from app.forms.project import ProjectForm
from datetime import datetime

bp = Blueprint('projects', __name__, url_prefix='/projects')

@bp.route('/')
def list():
    projects = ResearchProject.query.order_by(ResearchProject.start_date.desc()).all()
    return render_template('projects/list.html', projects=projects)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    form = ProjectForm()
    
    # Populate researchers choices
    form.researchers.choices = [(r.researcher_id, f"{r.first_name} {r.last_name}") 
                              for r in Researcher.query.order_by(Researcher.first_name).all()]
    
    if form.validate_on_submit():
        project = ResearchProject(
            project_name=form.project_name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            status=form.status.data,
            funding_source=form.funding_source.data
        )
        
        # Add selected researchers
        selected_researchers = Researcher.query.filter(
            Researcher.researcher_id.in_(form.researchers.data)
        ).all()
        project.researchers = selected_researchers
        
        try:
            db.session.add(project)
            db.session.commit()
            flash('Project added successfully!', 'success')
            return redirect(url_for('projects.list'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding project. Please try again.', 'danger')
    
    return render_template('projects/form.html', form=form)

@bp.route('/<int:project_id>')
def view(project_id):
    project = ResearchProject.query.get_or_404(project_id)
    return render_template('projects/view.html', project=project)

@bp.route('/<int:project_id>/edit', methods=['GET', 'POST'])
def edit(project_id):
    project = ResearchProject.query.get_or_404(project_id)
    form = ProjectForm(obj=project)
    
    # Populate researchers choices
    form.researchers.choices = [(r.researcher_id, f"{r.first_name} {r.last_name}") 
                              for r in Researcher.query.order_by(Researcher.first_name).all()]
    
    if request.method == 'GET':
        # Set the selected researchers
        form.researchers.data = [r.researcher_id for r in project.researchers]
    
    if form.validate_on_submit():
        project.project_name = form.project_name.data
        project.description = form.description.data
        project.start_date = form.start_date.data
        project.end_date = form.end_date.data
        project.status = form.status.data
        project.funding_source = form.funding_source.data
        
        # Update researchers
        selected_researchers = Researcher.query.filter(
            Researcher.researcher_id.in_(form.researchers.data)
        ).all()
        project.researchers = selected_researchers
        
        try:
            db.session.commit()
            flash('Project updated successfully!', 'success')
            return redirect(url_for('projects.list'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating project. Please try again.', 'danger')
    
    return render_template('projects/form.html', form=form, project=project)

@bp.route('/<int:project_id>/delete', methods=['POST'])
def delete(project_id):
    project = ResearchProject.query.get_or_404(project_id)
    try:
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting project. Please try again.', 'danger')
    return redirect(url_for('projects.list')) 