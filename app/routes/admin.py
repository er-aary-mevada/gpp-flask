from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_security import roles_required, current_user
from flask_security.utils import hash_password
from ..models.user import User, Role
from ..models.department import Department
from ..models.project import Project
from ..forms.admin import UserCreationForm, BulkUserUploadForm
from ..extensions import db
from datetime import datetime
import pandas as pd
import os
from flask import current_app

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@roles_required('admin')
def index():
    # Get all users and pending users
    pending_users = User.query.filter_by(is_approved=False).all()
    
    # Get users by role
    hod_role = Role.query.filter_by(name='hod').first()
    lecturer_role = Role.query.filter_by(name='lecturer').first()
    student_role = Role.query.filter_by(name='student').first()
    lab_assistant_role = Role.query.filter_by(name='lab_assistant').first()
    librarian_role = Role.query.filter_by(name='librarian').first()
    store_officer_role = Role.query.filter_by(name='store_officer').first()
    
    hods = User.query.filter(User.roles.contains(hod_role)).all() if hod_role else []
    lecturers = User.query.filter(User.roles.contains(lecturer_role)).all() if lecturer_role else []
    students = User.query.filter(User.roles.contains(student_role)).all() if student_role else []
    lab_assistants = User.query.filter(User.roles.contains(lab_assistant_role)).all() if lab_assistant_role else []
    librarians = User.query.filter(User.roles.contains(librarian_role)).all() if librarian_role else []
    store_officers = User.query.filter(User.roles.contains(store_officer_role)).all() if store_officer_role else []
    
    # Get departments
    departments = Department.query.all()
    
    # Get projects
    projects = Project.query.all()
    
    return render_template('admin/index.html', 
                         pending_users=pending_users,
                         hods=hods,
                         lecturers=lecturers,
                         students=students,
                         lab_assistants=lab_assistants,
                         librarians=librarians,
                         store_officers=store_officers,
                         departments=departments,
                         projects=projects)

@bp.route('/approve_user/<int:user_id>', methods=['POST'])
@roles_required('admin')
def approve_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    user.approval_date = datetime.utcnow()
    user.approved_by = current_user
    db.session.commit()
    flash(f'User {user.email} has been approved.', 'success')
    return redirect(url_for('admin.index'))

@bp.route('/reject_user/<int:user_id>', methods=['POST'])
@roles_required('admin')
def reject_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.email} has been rejected and removed.', 'success')
    return redirect(url_for('admin.index'))

@bp.route('/create_department', methods=['POST'])
@roles_required('admin')
def create_department():
    name = request.form.get('name')
    hod_id = request.form.get('hod_id')
    
    if not name:
        flash('Department name is required.', 'error')
        return redirect(url_for('admin.index', _anchor='departments'))
    
    if Department.query.filter_by(name=name).first():
        flash('Department with this name already exists.', 'error')
        return redirect(url_for('admin.index', _anchor='departments'))
    
    department = Department(name=name)
    if hod_id:
        department.hod_id = hod_id
    
    db.session.add(department)
    db.session.commit()
    
    flash(f'Department {name} has been created.', 'success')
    return redirect(url_for('admin.index', _anchor='departments'))

@bp.route('/edit_department/<int:dept_id>', methods=['POST'])
@roles_required('admin')
def edit_department(dept_id):
    department = Department.query.get_or_404(dept_id)
    name = request.form.get('name')
    hod_id = request.form.get('hod_id')
    
    if not name:
        flash('Department name is required.', 'error')
        return redirect(url_for('admin.index', _anchor='departments'))
    
    existing = Department.query.filter_by(name=name).first()
    if existing and existing.id != dept_id:
        flash('Department with this name already exists.', 'error')
        return redirect(url_for('admin.index', _anchor='departments'))
    
    department.name = name
    department.hod_id = hod_id if hod_id else None
    db.session.commit()
    
    flash(f'Department {name} has been updated.', 'success')
    return redirect(url_for('admin.index', _anchor='departments'))

@bp.route('/delete_department/<int:dept_id>', methods=['POST'])
@roles_required('admin')
def delete_department(dept_id):
    department = Department.query.get_or_404(dept_id)
    name = department.name
    
    # Check if department has any users
    if department.students or department.lecturers:
        flash('Cannot delete department that has users assigned to it.', 'error')
        return redirect(url_for('admin.index', _anchor='departments'))
    
    db.session.delete(department)
    db.session.commit()
    
    flash(f'Department {name} has been deleted.', 'success')
    return redirect(url_for('admin.index', _anchor='departments'))

@bp.route('/create_user', methods=['GET', 'POST'])
@roles_required('admin')
def create_user():
    form = UserCreationForm()
    
    # Pre-select roles if provided in query parameter
    role = request.args.get('role')
    if role and request.method == 'GET':
        form.roles.data = [role]  # Set as a list since it's a multiple select field
    
    if form.validate_on_submit():
        # Get the department
        department = Department.query.get(form.department.data) if form.department.data != 0 else None
        
        # Get or create the roles
        user_roles = []
        for role_name in form.roles.data:
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                role = Role(name=role_name)
                db.session.add(role)
                db.session.flush()  # Get the ID without committing
            user_roles.append(role)
        
        user = User(
            email=form.email.data,
            password=hash_password('changeme123'),  # Temporary password
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            department_id=department.id if department else None,
            active=True,
            is_approved=True,
            approval_date=datetime.utcnow(),
            approved_by=current_user
        )
        # Set the roles after user creation
        user.roles = user_roles
        
        db.session.add(user)
        db.session.commit()
        flash(f'User {user.email} has been created. Temporary password: changeme123', 'success')
        return redirect(url_for('admin.index'))
    
    # Get departments for the template context
    departments = Department.query.order_by(Department.name).all()
    return render_template('admin/create_user.html', form=form, departments=departments)

@bp.route('/bulk_upload', methods=['GET', 'POST'])
@roles_required('admin')
def bulk_upload():
    form = BulkUserUploadForm()
    if form.validate_on_submit():
        try:
            df = pd.read_csv(request.files[form.file.name])
            
            # Get or create selected roles
            user_roles = []
            for role_name in form.roles.data:
                role = Role.query.filter_by(name=role_name).first()
                if not role:
                    role = Role(name=role_name)
                    db.session.add(role)
                    db.session.flush()
                user_roles.append(role)
            
            success_count = 0
            error_count = 0
            
            for _, row in df.iterrows():
                try:
                    # Check if user already exists
                    if User.query.filter_by(email=row['email']).first():
                        error_count += 1
                        continue
                    
                    # Get or create department
                    department = None
                    if 'department' in row and row['department']:
                        department = Department.query.filter_by(name=row['department']).first()
                        if not department:
                            department = Department(name=row['department'])
                            db.session.add(department)
                            db.session.flush()  # Get the ID without committing
                    
                    # Handle additional roles from CSV if present
                    roles_to_assign = user_roles.copy()  # Start with the roles selected in the form
                    if 'roles' in row and row['roles']:
                        additional_role_names = [r.strip() for r in str(row['roles']).split(',')]
                        for role_name in additional_role_names:
                            if role_name:  # Skip empty strings
                                role = Role.query.filter_by(name=role_name).first()
                                if not role:
                                    role = Role(name=role_name)
                                    db.session.add(role)
                                    db.session.flush()
                                if role not in roles_to_assign:
                                    roles_to_assign.append(role)
                    
                    user = User(
                        email=row['email'],
                        password=hash_password('changeme123'),  # Temporary password
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        phone=str(row['phone']),
                        department_id=department.id if department else None,
                        active=True,
                        is_approved=True,
                        approval_date=datetime.utcnow(),
                        approved_by=current_user,
                        roles=roles_to_assign
                    )
                    db.session.add(user)
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    continue
            
            db.session.commit()
            flash(f'Bulk upload completed. {success_count} users created, {error_count} failed. '
                  f'Temporary password for all users: changeme123', 'success')
            return redirect(url_for('admin.index'))
            
        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'error')
            return redirect(url_for('admin.index'))
    
    return render_template('admin/bulk_upload.html', form=form)

@bp.route('/api/departments/<int:dept_id>')
@roles_required('admin')
def get_department(dept_id):
    department = Department.query.get_or_404(dept_id)
    return jsonify({
        'id': department.id,
        'name': department.name,
        'hod_id': department.hod_id if department.hod else None
    })

@bp.route('/project/<int:project_id>')
@roles_required('admin')
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify({
        'id': project.id,
        'name': project.name,
        'description': project.description,
        'department_id': project.department_id,
        'group_leader': project.group_leader,
        'members': project.members,
        'marks': project.marks
    })

@bp.route('/create_project', methods=['POST'])
@roles_required('admin')
def create_project():
    name = request.form.get('name')
    if not name:
        flash('Project name is required.', 'error')
        return redirect(url_for('admin.index', _anchor='projects'))
    
    project = Project(
        name=name,
        description=request.form.get('description', ''),
        department_id=request.form.get('department_id'),
        group_leader=request.form.get('group_leader'),
        members=request.form.get('members'),
        marks=None  # Marks will be added through Jury file
    )
    
    db.session.add(project)
    db.session.commit()
    
    flash(f'Project {name} has been created.', 'success')
    return redirect(url_for('admin.index', _anchor='projects'))

@bp.route('/edit_project/<int:project_id>', methods=['POST'])
@roles_required('admin')
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    name = request.form.get('name')
    if not name:
        flash('Project name is required.', 'error')
        return redirect(url_for('admin.index', _anchor='projects'))
    
    project.name = name
    project.description = request.form.get('description', '')
    project.department_id = request.form.get('department_id')
    project.group_leader = request.form.get('group_leader')
    project.members = request.form.get('members')
    # Don't update marks - they will be added through Jury file
    
    db.session.commit()
    
    flash(f'Project {name} has been updated.', 'success')
    return redirect(url_for('admin.index', _anchor='projects'))

@bp.route('/delete_project/<int:project_id>', methods=['POST'])
@roles_required('admin')
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    name = project.name
    
    db.session.delete(project)
    db.session.commit()
    
    flash(f'Project {name} has been deleted.', 'success')
    return redirect(url_for('admin.index', _anchor='projects'))

@bp.route('/import_projects', methods=['POST'])
@roles_required('admin')
def import_projects():
    if 'csv_file' not in request.files:
        flash('No file uploaded.', 'error')
        return redirect(url_for('admin.index', _anchor='projects'))
    
    file = request.files['csv_file']
    if file.filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('admin.index', _anchor='projects'))
    
    if not file.filename.endswith('.csv'):
        flash('Please upload a CSV file.', 'error')
        return redirect(url_for('admin.index', _anchor='projects'))
    
    try:
        # Save the file temporarily
        temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp.csv')
        file.save(temp_path)
        
        # Import projects from CSV
        projects = Project.import_from_csv(temp_path)
        
        # Add all projects to database
        for project in projects:
            db.session.add(project)
        
        db.session.commit()
        os.remove(temp_path)  # Clean up temp file
        
        flash(f'Successfully imported {len(projects)} projects.', 'success')
    except Exception as e:
        flash(f'Error importing projects: {str(e)}', 'error')
    
    return redirect(url_for('admin.index', _anchor='projects'))

@bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@roles_required('admin')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserCreationForm(obj=user)
    
    if request.method == 'GET':
        form.department.data = user.department_id if user.department else 0
        form.roles.data = [role.name for role in user.roles]
    
    if form.validate_on_submit():
        # Get the department
        department = Department.query.get(form.department.data) if form.department.data != 0 else None
        
        # Get or create the roles
        user_roles = []
        for role_name in form.roles.data:
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                role = Role(name=role_name)
                db.session.add(role)
                db.session.flush()
            user_roles.append(role)
        
        # Update user details
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.phone = form.phone.data
        user.department_id = department.id if department else None
        user.roles = user_roles
        
        db.session.commit()
        flash(f'User {user.email} has been updated.', 'success')
        return redirect(url_for('admin.index'))
    
    return render_template('admin/edit_user.html', form=form, user=user)

@bp.route('/delete_user/<int:user_id>', methods=['POST'])
@roles_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    email = user.email
    db.session.delete(user)
    db.session.commit()
    flash(f'User {email} has been deleted.', 'success')
    return redirect(url_for('admin.index'))
