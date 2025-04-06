from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app.models.ssip_submission import SSIPSubmission
from app.models.ssip_workflow import SSIPWorkflow
from app.models.department import Department
from app.extensions import db
from functools import wraps

bp = Blueprint('ssip_coordinator', __name__)

def coordinator_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.has_role('lecturer'):
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/ssip-submissions')
@login_required
@coordinator_required
def view_submissions():
    # For department coordinators, show only their department's submissions
    if current_user.department_id:
        submissions = SSIPSubmission.query.filter_by(
            department_id=current_user.department_id
        ).order_by(SSIPSubmission.created_at.desc()).all()
        is_dept_coordinator = True
    else:
        # For college coordinators, show all submissions
        submissions = SSIPSubmission.query.order_by(
            SSIPSubmission.created_at.desc()
        ).all()
        is_dept_coordinator = False
    
    return render_template(
        'ssip_coordinator/submissions.html',
        submissions=submissions,
        is_dept_coordinator=is_dept_coordinator
    )

@bp.route('/ssip-submission/<int:id>')
@login_required
@coordinator_required
def view_submission(id):
    submission = SSIPSubmission.query.get_or_404(id)
    
    # Department coordinators can only view their department's submissions
    if current_user.department_id and submission.department_id != current_user.department_id:
        flash('You do not have permission to view this submission.', 'error')
        return redirect(url_for('ssip_coordinator.view_submissions'))
    
    return render_template(
        'ssip_coordinator/submission_details.html',
        submission=submission
    )

@bp.route('/ssip-submission/<int:id>/update-status', methods=['POST'])
@login_required
@coordinator_required
def update_submission_status(id):
    try:
        submission = SSIPSubmission.query.get_or_404(id)
        
        # Department coordinators can only update their department's submissions
        if current_user.department_id and submission.department_id != current_user.department_id:
            return jsonify({'error': 'Permission denied'}), 403
        
        status = request.form.get('status')
        remarks = request.form.get('remarks', '')
        needs_revision = request.form.get('needs_revision') == 'on'
        
        if not status:
            return jsonify({'error': 'Status is required'}), 400
        
        # Update submission status and remarks
        submission.status = 'revision_needed' if needs_revision else status
        submission.remarks = remarks
        
        # Create or get workflow
        workflow = submission.workflow
        if not workflow:
            workflow = SSIPWorkflow(
                submission_id=submission.id,
                current_reviewer='department',
                dept_status=None,
                college_status=None,
                principal_status=None
            )
            db.session.add(workflow)
            submission.workflow = workflow
            db.session.flush()
        
        # Handle workflow based on user role and status
        if current_user.department_id == submission.department_id:  # Department coordinator
            if needs_revision:
                workflow.current_reviewer = None  # Back to student
            else:
                workflow.dept_status = status
                workflow.dept_remarks = remarks
                workflow.dept_action_date = datetime.utcnow()
                workflow.dept_coordinator_id = current_user.id
                workflow.current_reviewer = 'college' if status == 'approved' else None
        
        elif current_user.has_role('principal'):  # Principal
            if needs_revision:
                workflow.current_reviewer = None  # Back to student
            else:
                workflow.principal_status = status
                workflow.principal_remarks = remarks
                workflow.principal_action_date = datetime.utcnow()
                workflow.principal_id = current_user.id
                workflow.current_reviewer = None  # End of workflow
        
        else:  # College coordinator
            if needs_revision:
                workflow.current_reviewer = None  # Back to student
            else:
                workflow.college_status = status
                workflow.college_remarks = remarks
                workflow.college_action_date = datetime.utcnow()
                workflow.college_coordinator_id = current_user.id
                workflow.current_reviewer = 'principal' if status == 'approved' else None
        
        db.session.commit()
        
        return jsonify({
            'message': 'Status updated successfully',
            'new_status': submission.status,
            'workflow_stage': workflow.current_reviewer
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
