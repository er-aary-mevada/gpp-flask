from flask import Blueprint, render_template
from flask_security import login_required, current_user
from ..models.user import User, Role
from ..models.department import Department
from ..extensions import db

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def index():
    if current_user.has_role('admin'):
        # Get stats for admin dashboard
        stats = {
            'students': User.query.join(User.roles).filter(Role.name == 'student').count(),
            'lecturers': User.query.join(User.roles).filter(Role.name == 'lecturer').count(),
            'departments': Department.query.count(),
            'pending_approvals': User.query.filter_by(is_approved=False).count()
        }
        
        # Get recent activity (placeholder for now)
        recent_activity = []
        
        return render_template('dashboard/admin.html', stats=stats, recent_activity=recent_activity)
    
    role = current_user.roles[0].name if current_user.roles else None
    template = f'dashboard/{role}.html' if role else 'dashboard/user.html'
    
    try:
        return render_template(template)
    except:
        # Fallback to default dashboard if role-specific template doesn't exist
        return render_template('dashboard/default.html')
