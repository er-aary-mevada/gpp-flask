from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models.ssip_submission import SSIPSubmission
from app.models.department import Department
from app.forms.ssip import SSIPSubmissionForm
from app.extensions import db
import json
import os

bp = Blueprint('ssip', __name__)

@bp.route('/ssip')
@login_required
def index():
    return render_template('ssip/index.html')

@bp.route('/submit-idea', methods=['GET', 'POST'])
@login_required
def submit_idea():
    form = SSIPSubmissionForm()
    
    # Populate department choices
    departments = Department.query.all()
    form.department_id.choices = [(0, 'Select Department')] + [(d.id, d.name) for d in departments]
    
    if form.validate_on_submit():
        # Handle file uploads
        files = {}
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'ssip_submissions')
        os.makedirs(upload_dir, exist_ok=True)
        
        for field in ['proposal_document', 'presentation', 'additional_documents']:
            file = getattr(form, field).data
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(upload_dir, filename)
                file.save(file_path)
                files[field] = filename
        
        # Create new submission
        submission = SSIPSubmission(
            project_title=form.project_title.data,
            team_name=form.team_name.data,
            student_name=form.student_name.data,
            enrollment_number=form.enrollment_number.data,
            contact_number=form.contact_number.data,
            email=form.email.data,
            department_id=form.department_id.data,
            semester=form.semester.data,
            problem_statement=form.problem_statement.data,
            solution_description=form.solution_description.data,
            innovation_description=form.innovation_description.data,
            technical_description=form.technical_description.data,
            project_category=form.project_category.data,
            estimated_project_cost=form.estimated_project_cost.data,
            fund_requirement_description=form.fund_requirement_description.data,
            current_stage=form.current_stage.data,
            completion_time=form.completion_time.data,
            mentor_name=form.mentor_name.data,
            mentor_designation=form.mentor_designation.data,
            team_members=json.dumps([member.data for member in form.team_members if member.data]),
            status='pending'
        )
        
        db.session.add(submission)
        db.session.commit()
        
        flash('Your SSIP project proposal has been submitted successfully!', 'success')
        return redirect(url_for('ssip.my_projects'))
    
    return render_template('ssip/submit_idea.html', form=form)

@bp.route('/my-projects')
@login_required
def my_projects():
    submissions = SSIPSubmission.query.filter_by(email=current_user.email).all()
    return render_template('ssip/my_projects.html', submissions=submissions)

@bp.route('/guidelines')
@login_required
def guidelines():
    return render_template('ssip/guidelines.html')
