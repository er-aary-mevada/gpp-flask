from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models.ssip_submission import SSIPSubmission
from app.models.ssip_workflow import SSIPWorkflow
from app.models.department import Department
from app.forms.ssip import SSIPSubmissionForm
from app.forms.ssip_fund import FundRequestForm, UtilizationForm
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
        
        # Create submission
        db.session.add(submission)
        db.session.flush()
        
        # Create workflow
        workflow = SSIPWorkflow(
            submission_id=submission.id,
            current_reviewer='department'  # Start with department review
        )
        db.session.add(workflow)
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

@bp.route('/fund-request-form', methods=['GET', 'POST'])
@login_required
def fund_request_form():
    form = FundRequestForm()
    if form.validate_on_submit():
        # Create upload directory
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'ssip_fund_requests')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Process form data and save files
        files = {}
        for item in form.items:
            quotations = item.quotations.data
            if quotations:
                filename = secure_filename(quotations.filename)
                file_path = os.path.join(upload_dir, filename)
                quotations.save(file_path)
                files[f'quotation_{item.item_name.data}'] = filename
        
        # Save mentor signature
        if form.mentor_signature.data:
            filename = secure_filename(form.mentor_signature.data.filename)
            file_path = os.path.join(upload_dir, filename)
            form.mentor_signature.data.save(file_path)
            files['mentor_signature'] = filename
        
        # TODO: Save form data to database
        # This would require creating appropriate database models
        
        flash('Fund request submitted successfully!', 'success')
        return redirect(url_for('ssip.my_projects'))
    
    return render_template('ssip/fund_request_form.html', form=form)

@bp.route('/utilization-form', methods=['GET', 'POST'])
@login_required
def utilization_form():
    form = UtilizationForm()
    if form.validate_on_submit():
        # Create upload directory
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'ssip_utilization')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Process form data and save files
        files = {}
        for item in form.items:
            invoice = item.invoice.data
            if invoice:
                filename = secure_filename(invoice.filename)
                file_path = os.path.join(upload_dir, filename)
                invoice.save(file_path)
                files[f'invoice_{item.item_name.data}'] = filename
        
        # Save signatures
        for field in ['team_leader_signature', 'mentor_signature', 
                     'dept_coordinator_signature', 'finance_member_signature']:
            file = getattr(form, field).data
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(upload_dir, filename)
                file.save(file_path)
                files[field] = filename
        
        # TODO: Save form data to database
        # This would require creating appropriate database models
        
        flash('Utilization certificate submitted successfully!', 'success')
        return redirect(url_for('ssip.my_projects'))
    
    return render_template('ssip/utilization_form.html', form=form)

@bp.route('/submission/<int:id>')
@login_required
def view_submission(id):
    submission = SSIPSubmission.query.get_or_404(id)
    
    # Check if user has permission to view this submission
    if current_user.email != submission.email and not current_user.has_role('coordinator'):
        flash('You do not have permission to view this submission.', 'error')
        return redirect(url_for('main.dashboard'))
    
    return render_template('ssip/view_submission.html', submission=submission)

@bp.route('/coordinator/pending-submissions')
@login_required
def pending_submissions():
    if not current_user.has_role('coordinator'):
        flash('Unauthorized access', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Get submissions based on coordinator role
    if current_user.department_id:  # Department coordinator
        submissions = SSIPSubmission.query.join(SSIPWorkflow).filter(
            SSIPSubmission.department_id == current_user.department_id,
            SSIPWorkflow.current_reviewer == 'department'
        ).all()
    elif current_user.has_role('principal'):  # Principal
        submissions = SSIPSubmission.query.join(SSIPWorkflow).filter(
            SSIPWorkflow.current_reviewer == 'principal'
        ).all()
    else:  # College coordinator
        submissions = SSIPSubmission.query.join(SSIPWorkflow).filter(
            SSIPWorkflow.current_reviewer == 'college'
        ).all()
    
    return render_template('ssip/coordinator/pending_submissions.html', submissions=submissions)

@bp.route('/ssip-coordinator/ssip-submission/<int:id>/update-status', methods=['POST'])
@login_required
def update_submission_status(id):
    if not current_user.has_role('coordinator'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        submission = SSIPSubmission.query.get_or_404(id)
        new_status = request.form.get('status')
        remarks = request.form.get('remarks', '')
        needs_revision = request.form.get('needs_revision') == 'true'
        
        if not new_status:
            return jsonify({'error': 'Status is required'}), 400
        
        # Update submission status and remarks
        submission.status = 'revision_needed' if needs_revision else new_status
        submission.remarks = remarks
        
        # Update workflow
        if not submission.workflow:
            workflow = SSIPWorkflow(
                submission_id=submission.id,
                current_reviewer='department'
            )
            db.session.add(workflow)
            db.session.flush()
        
        # Handle workflow based on user role and status
        if current_user.department_id == submission.department_id:  # Department coordinator
            if needs_revision:
                submission.workflow.current_reviewer = None  # Back to student
            else:
                submission.workflow.dept_status = new_status
                submission.workflow.dept_remarks = remarks
                submission.workflow.dept_action_date = datetime.utcnow()
                submission.workflow.dept_coordinator_id = current_user.id
                submission.workflow.current_reviewer = 'college' if new_status == 'approved' else None
        
        elif current_user.has_role('principal'):  # Principal
            if needs_revision:
                submission.workflow.current_reviewer = None  # Back to student
            else:
                submission.workflow.principal_status = new_status
                submission.workflow.principal_remarks = remarks
                submission.workflow.principal_action_date = datetime.utcnow()
                submission.workflow.principal_id = current_user.id
                submission.workflow.current_reviewer = None  # End of workflow
        
        else:  # College coordinator
            if needs_revision:
                submission.workflow.current_reviewer = None  # Back to student
            else:
                submission.workflow.college_status = new_status
                submission.workflow.college_remarks = remarks
                submission.workflow.college_action_date = datetime.utcnow()
                submission.workflow.college_coordinator_id = current_user.id
                submission.workflow.current_reviewer = 'principal' if new_status == 'approved' else None
        
        db.session.commit()
        
        # Send notification (you'll need to implement this)
        # notify_status_change(submission)
        
        return jsonify({
            'message': 'Status updated successfully',
            'new_status': submission.status,
            'workflow_stage': submission.workflow.current_reviewer
        })
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error updating submission status: {str(e)}')
        return jsonify({'error': str(e)}), 500

@bp.route('/submission/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_submission(id):
    submission = SSIPSubmission.query.get_or_404(id)
    
    # Check if user can edit
    if current_user.email != submission.email:
        flash('You are not authorized to edit this submission', 'error')
        return redirect(url_for('ssip.my_projects'))
    
    # Check if submission is in editable state
    if submission.status != 'revision_needed':
        flash('This submission cannot be edited at this time', 'error')
        return redirect(url_for('ssip.my_projects'))
    
    # Populate department choices
    departments = Department.query.all()
    form = SSIPSubmissionForm()
    form.department_id.choices = [(0, 'Select Department')] + [(d.id, d.name) for d in departments]
    
    if request.method == 'GET':
        # Pre-populate form data
        for field in form._fields:
            if field not in ['csrf_token', 'team_members', 'proposal_document', 'presentation', 'additional_documents']:
                try:
                    setattr(form[field], 'data', getattr(submission, field))
                except AttributeError:
                    continue
        
        # Handle team members separately
        team_members = json.loads(submission.team_members) if submission.team_members else []
        while len(form.team_members) < len(team_members):
            form.team_members.append_entry()
        for i, member in enumerate(team_members):
            form.team_members[i].data = member
    
    if form.validate_on_submit():
        # Update submission fields except team_members and file fields
        for field in form._fields:
            if field not in ['csrf_token', 'team_members', 'proposal_document', 'presentation', 'additional_documents']:
                try:
                    setattr(submission, field, getattr(form, field).data)
                except AttributeError:
                    continue
        
        # Handle team members separately
        submission.team_members = json.dumps([member.data for member in form.team_members if member.data])
        
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
        
        submission.status = 'pending'
        
        # Reset workflow to department review
        submission.workflow.current_reviewer = 'department'
        
        db.session.commit()
        flash('Your submission has been updated successfully', 'success')
        return redirect(url_for('ssip.my_projects'))
    
    return render_template('ssip/edit_submission.html', form=form, submission=submission)
