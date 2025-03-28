from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.result import Result
from app.models.user import User

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    return redirect(url_for('main.dashboard'))

@bp.route('/dashboard/')
@login_required
def dashboard():
    if current_user.has_role('admin'):
        # Get stats for admin dashboard
        stats = {
            'students': User.query.filter(User.roles.any(name='student')).count(),
            'total_results': Result.query.count(),
            'recent_results': Result.query.order_by(Result.declaration_date.desc()).limit(5).all()
        }
        return render_template('dashboard/admin.html', stats=stats)
    elif current_user.has_role('student'):
        # Get latest result for the student
        latest_result = Result.query.filter_by(
            student_id=current_user.student_id
        ).order_by(Result.declaration_date.desc()).first()
        
        return render_template('dashboard/student.html', latest_result=latest_result)
    else:
        return render_template('dashboard/default.html')
