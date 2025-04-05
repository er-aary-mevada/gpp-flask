from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app.models.ssip_submission import SSIPSubmission
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
    submission = SSIPSubmission.query.get_or_404(id)
    
    # Department coordinators can only update their department's submissions
    if current_user.department_id and submission.department_id != current_user.department_id:
        return jsonify({'error': 'Permission denied'}), 403
    
    status = request.form.get('status')
    remarks = request.form.get('remarks')
    
    if status not in ['pending', 'approved', 'rejected']:
        return jsonify({'error': 'Invalid status'}), 400
    
    submission.status = status
    submission.remarks = remarks
    db.session.commit()
    
    flash(f'Submission status updated to {status}.', 'success')
    return jsonify({'success': True})
