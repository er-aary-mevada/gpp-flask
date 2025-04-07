from app import create_app
from app.extensions import db
from app.models.user import User, Role
from app.models.department import Department
from app.models.project import Project
from flask_security.utils import hash_password
from datetime import datetime
import argparse

app = create_app()

def init_base():
    """Initialize basic database structure and roles."""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create default roles if they don't exist
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', description='Administrator')
            db.session.add(admin_role)
        
        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            user_role = Role(name='user', description='Regular User')
            db.session.add(user_role)
        
        # Create default department if it doesn't exist
        default_dept = Department.query.filter_by(name='General').first()
        if not default_dept:
            default_dept = Department(name='General')
            db.session.add(default_dept)
        
        db.session.commit()
        print("Base database initialized successfully!")

def create_admin():
    """Create admin user if it doesn't exist."""
    with app.app_context():
        # Get admin role
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            print("Error: Admin role not found. Please run init_base first.")
            return False

        # Check if admin user exists
        admin_email = 'admin@gppalanpur.in'
        admin_user = User.query.filter_by(email=admin_email).first()
        
        if not admin_user:
            admin_user = User(
                email=admin_email,
                password=hash_password('admin123'),  # Default password
                active=True,
                is_approved=True,
                first_name='Admin',
                last_name='User',
                confirmed_at=datetime.utcnow(),
                roles=[admin_role]
            )
            db.session.add(admin_user)
            db.session.commit()
            print(f"Admin user created successfully with email: {admin_email}")
            print("Default password: admin123")
            return True
        else:
            print("Admin user already exists")
            return True

def create_departments():
    """Create sample departments."""
    departments = [
        'Computer Engineering',
        'Mechanical Engineering',
        'Civil Engineering',
        'Electrical Engineering',
        'Chemical Engineering',
        'Electronics Engineering',
        'Information Technology',
        'Automobile Engineering'
    ]
    
    with app.app_context():
        for dept_name in departments:
            dept = Department.query.filter_by(name=dept_name).first()
            if not dept:
                dept = Department(name=dept_name)
                db.session.add(dept)
                print(f"Added department: {dept_name}")
        
        db.session.commit()
        print("Sample departments created successfully!")

def create_sample_projects():
    """Create sample projects for Computer Engineering department."""
    with app.app_context():
        # Get Computer Engineering department
        dept = Department.query.filter_by(name='Computer Engineering').first()
        if not dept:
            print("Error: Computer Engineering department not found. Please create departments first.")
            return False

        # Sample projects
        sample_projects = [
            {
                'title': 'Smart Library Management System',
                'description': 'Developing a digital library management system with RFID integration for efficient book tracking and management.',
                'department_id': dept.id,
                'group_leader': 'Raj Patel',
                'members': 'Raj Patel, Priya Shah, Amit Kumar, Neha Singh',
                'status': 'pending',
                'marks': None,
                'presentation_type': 'Demo Model',
                'semester': '6th Sem',
                'faculty_mentor': 'Prof. Shah',
                'mobile_number': '9876543211',
                'submission_timestamp': datetime.now()
            },
            {
                'title': 'Student Attendance App',
                'description': 'Mobile application for tracking student attendance using biometric authentication.',
                'department_id': dept.id,
                'group_leader': 'Kunal Shah',
                'members': 'Kunal Shah, Pooja Patel, Rohan Joshi, Sneha Kumar',
                'status': 'pending',
                'marks': None,
                'presentation_type': 'Demo Model',
                'semester': '6th Sem',
                'faculty_mentor': 'Dr. Patel',
                'mobile_number': '9876543212',
                'submission_timestamp': datetime.now()
            },
            {
                'title': 'College Event Portal',
                'description': 'Web portal for managing college events, registrations, and generating attendance certificates.',
                'department_id': dept.id,
                'group_leader': 'Anita Desai',
                'members': 'Anita Desai, Rahul Patel, Kiran Shah, Maya Singh',
                'status': 'pending',
                'marks': None,
                'presentation_type': 'Demo Model',
                'semester': '6th Sem',
                'faculty_mentor': 'Prof. Kumar',
                'mobile_number': '9876543213',
                'submission_timestamp': datetime.now()
            },
            {
                'title': 'Lab Equipment Tracker',
                'description': 'System to track and manage laboratory equipment, maintenance schedules, and usage logs.',
                'department_id': dept.id,
                'group_leader': 'Vikram Mehta',
                'members': 'Vikram Mehta, Nisha Patel, Arun Kumar, Divya Shah',
                'status': 'pending',
                'marks': None,
                'presentation_type': 'Demo Model',
                'semester': '6th Sem',
                'faculty_mentor': 'Dr. Singh',
                'mobile_number': '9876543214',
                'submission_timestamp': datetime.now()
            }
        ]

        # Add projects to database
        for project_data in sample_projects:
            project = Project.query.filter_by(title=project_data['title']).first()
            if not project:
                project = Project(**project_data)
                db.session.add(project)
                print(f"Added project: {project_data['title']}")
        
        db.session.commit()
        print("Sample projects created successfully!")
        return True

def create_ssip_lecturers():
    """Create SSIP handling lecturers - one for department level and one for college level."""
    with app.app_context():
        # Get lecturer role
        lecturer_role = Role.query.filter_by(name='lecturer').first()
        if not lecturer_role:
            lecturer_role = Role(name='lecturer', description='Lecturer')
            db.session.add(lecturer_role)
            db.session.commit()

        # Get Computer Engineering department
        comp_dept = Department.query.filter_by(name='Computer Engineering').first()
        if not comp_dept:
            print("Error: Computer Engineering department not found")
            return False

        # Create department level SSIP coordinator
        dept_coordinator = User.query.filter_by(email='dept.ssip@gppalanpur.in').first()
        if not dept_coordinator:
            dept_coordinator = User(
                email='dept.ssip@gppalanpur.in',
                password=hash_password('ssip123'),
                active=True,
                is_approved=True,
                first_name='Department',
                last_name='SSIP Coordinator',
                department_id=comp_dept.id,
                confirmed_at=datetime.utcnow(),
                roles=[lecturer_role]
            )
            db.session.add(dept_coordinator)

        # Create college level SSIP coordinator
        college_coordinator = User.query.filter_by(email='college.ssip@gppalanpur.in').first()
        if not college_coordinator:
            college_coordinator = User(
                email='college.ssip@gppalanpur.in',
                password=hash_password('ssip123'),
                active=True,
                is_approved=True,
                first_name='College',
                last_name='SSIP Coordinator',
                confirmed_at=datetime.utcnow(),
                roles=[lecturer_role]
            )
            db.session.add(college_coordinator)

        db.session.commit()
        print("SSIP coordinators created successfully!")
        print("Department SSIP Coordinator - Email: dept.ssip@gppalanpur.in, Password: ssip123")
        print("College SSIP Coordinator - Email: college.ssip@gppalanpur.in, Password: ssip123")
        return True

def init_all():
    """Initialize everything in the correct order."""
    print("Initializing database...")
    init_base()
    if create_admin():
        create_departments()
        create_sample_projects()
        create_ssip_lecturers()
    print("Database initialization complete!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Initialize the database with various options')
    parser.add_argument('--all', action='store_true', help='Initialize everything (default)')
    parser.add_argument('--base', action='store_true', help='Initialize base database structure only')
    parser.add_argument('--admin', action='store_true', help='Create admin user only')
    parser.add_argument('--departments', action='store_true', help='Create departments only')
    parser.add_argument('--projects', action='store_true', help='Create sample projects only')
    
    args = parser.parse_args()
    
    # If no arguments provided or --all specified, run everything
    if not any(vars(args).values()) or args.all:
        init_all()
    else:
        if args.base:
            init_base()
        if args.admin:
            create_admin()
        if args.departments:
            create_departments()
        if args.projects:
            create_sample_projects()
