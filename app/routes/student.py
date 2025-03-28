from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from app.models.result import Result

bp = Blueprint('student', __name__)

@bp.route('/my-results')
@login_required
def my_results():
    if not current_user.student_id:
        abort(403)  # Forbidden if user is not a student
        
    # Get all results for the student
    results = Result.query.filter_by(
        student_id=current_user.student_id
    ).order_by(Result.declaration_date.desc()).all()
    
    return render_template('student/my_results.html', results=results)

@bp.route('/my-result/<string:exam_id>')
@login_required
def view_result(exam_id):
    if not current_user.student_id:
        abort(403)
        
    result = Result.query.filter_by(
        student_id=current_user.student_id,
        exam_id=exam_id
    ).first_or_404()
    
    return render_template('student/result_view.html', result=result)
