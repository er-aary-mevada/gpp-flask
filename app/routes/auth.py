from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_security import current_user, login_required, logout_user
from flask_security.utils import hash_password, verify_password
from ..extensions import db
from ..forms.auth import ExtendedRegisterForm, LoginForm
from ..models.user import User, Role
from ..models.department import Department

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = ExtendedRegisterForm()
    if form.validate_on_submit():
        role = Role.query.filter_by(name=form.role.data).first()
        if not role:
            role = Role(name=form.role.data)
            db.session.add(role)
        
        # Get the department
        department = Department.query.get(form.department.data) if form.department.data != 0 else None
        
        user = User(
            email=form.email.data,
            password=hash_password(form.password.data),
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            department_id=department.id if department else None,
            active=True,
            roles=[role]
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful. Please wait for admin approval.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and verify_password(form.password.data, user.password):
            if not user.is_approved and not user.has_role('admin'):
                flash('Your account is pending approval.', 'error')
                return redirect(url_for('auth.login'))
            
            # Check if user has the selected role
            if not user.has_role(form.role.data):
                flash('You do not have permission to login with this role.', 'error')
                return redirect(url_for('auth.login'))
            
            login_user(user)
            flash('Logged in successfully.', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
        
        flash('Invalid email or password.', 'error')
    
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
