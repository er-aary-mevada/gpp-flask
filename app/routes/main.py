from flask import Blueprint, render_template, redirect, url_for, flash
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
            'total_users': User.query.count(),
            'total_students': User.query.filter(User.roles.any(name='student')).count(),
            'total_staff': User.query.filter(User.roles.any(name='staff')).count(),
            'total_results': Result.query.count(),
<<<<<<< HEAD
            'total_departments': Department.query.count(),
            'pending_approvals': User.query.filter_by(is_approved=False).count(),
            'recent_users': User.query.order_by(User.created_at.desc()).limit(5).all(),
            'recent_results': Result.query.order_by(Result.declaration_date.desc()).limit(5).all()
=======
            'recent_results': Result.query.join(Result.student).order_by(Result.declaration_date.desc()).limit(5).all()
>>>>>>> 8a7d3d539d4d2916465601d4460b529061a29dc8
        }
        return render_template('dashboard/admin.html', stats=stats)
    
    elif current_user.has_role('hod'):
        # Get stats for HOD dashboard
        dept_students = User.query.filter(
            User.roles.any(name='student'),
            User.department_id == current_user.department_id
        )
        dept_staff = User.query.filter(
            User.roles.any(name='staff'),
            User.department_id == current_user.department_id
        )
        stats = {
            'total_students': dept_students.count(),
            'total_staff': dept_staff.count(),
            'department': current_user.department,
            'recent_results': Result.query.join(User).filter(
                User.department_id == current_user.department_id
            ).order_by(Result.declaration_date.desc()).limit(5).all()
        }
        return render_template('dashboard/hod.html', stats=stats)
    
    elif current_user.has_role('lecturer'):
        # Get stats for lecturer dashboard
        dept_students = User.query.filter(
            User.roles.any(name='student'),
            User.department_id == current_user.department_id
        )
        stats = {
            'total_students': dept_students.count(),
            'department': current_user.department,
            'recent_results': Result.query.join(User).filter(
                User.department_id == current_user.department_id
            ).order_by(Result.declaration_date.desc()).limit(5).all()
        }
        return render_template('dashboard/lecturer.html', stats=stats)
    
    elif current_user.has_role('librarian'):
        stats = {
            'total_students': User.query.filter(User.roles.any(name='student')).count(),
            'total_staff': User.query.filter(User.roles.any(name='staff')).count(),
            'recent_users': User.query.order_by(User.created_at.desc()).limit(5).all()
        }
        return render_template('dashboard/librarian.html', stats=stats)
    
    elif current_user.has_role('lab_assistant'):
        dept_students = User.query.filter(
            User.roles.any(name='student'),
            User.department_id == current_user.department_id
        )
        stats = {
            'total_students': dept_students.count(),
            'department': current_user.department
        }
        return render_template('dashboard/lab_assistant.html', stats=stats)
    
    elif current_user.has_role('store_officer'):
        stats = {
            'total_departments': Department.query.count(),
            'departments': Department.query.all()
        }
        return render_template('dashboard/store_officer.html', stats=stats)
    
    elif current_user.has_role('student'):
        # Get latest result for the student
        latest_result = Result.query.filter_by(
            student_id=current_user.id
        ).order_by(Result.declaration_date.desc()).first()
        return render_template('dashboard/student.html', latest_result=latest_result)
    
    else:
        return render_template('dashboard/default.html')

@bp.route('/results')
@login_required
def view_results():
    if current_user.has_role('student'):
        results = Result.query.filter_by(student_id=current_user.id).order_by(Result.declaration_date.desc()).all()
        return render_template('student/results.html', results=results)
    else:
        flash('You do not have permission to view results.', 'error')
        return redirect(url_for('main.dashboard'))

@bp.route('/results/<int:result_id>')
@login_required
def view_result_details(result_id):
    if current_user.has_role('student'):
        result = Result.query.filter_by(id=result_id, student_id=current_user.id).first_or_404()
        return render_template('student/result_details.html', result=result)
    else:
        flash('You do not have permission to view this result.', 'error')
        return redirect(url_for('main.dashboard'))
