from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.models.project import Project
from app.extensions import db

bp = Blueprint('ssip', __name__)

@bp.route('/ssip')
@login_required
def index():
    return render_template('ssip/index.html')

@bp.route('/submit-idea', methods=['GET', 'POST'])
@login_required
def submit_idea():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        project = Project(
            title=title,
            description=description,
            student_id=current_user.id,
            status='pending'
        )
        db.session.add(project)
        db.session.commit()
        
        flash('Your idea has been submitted successfully!', 'success')
        return redirect(url_for('ssip.my_projects'))
        
    return render_template('ssip/submit_idea.html')

@bp.route('/my-projects')
@login_required
def my_projects():
    projects = Project.query.filter_by(student_id=current_user.id).all()
    return render_template('ssip/my_projects.html', projects=projects)

@bp.route('/guidelines')
@login_required
def guidelines():
    return render_template('ssip/guidelines.html')
