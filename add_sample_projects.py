from app import create_app
from app.extensions import db
from app.models.project import Project
from app.models.department import Department

app = create_app()

with app.app_context():
    # Create Computer Engineering department if it doesn't exist
    dept = Department.query.filter_by(name='Computer Engineering').first()
    if not dept:
        dept = Department(name='Computer Engineering')
        db.session.add(dept)
        db.session.commit()

    # Sample projects
    projects = [
        {
            'name': 'Smart Library Management System',
            'description': 'Developing a digital library management system with RFID integration for efficient book tracking and management.',
            'department_id': dept.id,
            'group_leader': 'Raj Patel',
            'members': 'Raj Patel, Priya Shah, Amit Kumar, Neha Singh',
            'marks': None
        },
        {
            'name': 'IoT Weather Station',
            'description': 'Building a weather monitoring station using IoT sensors to collect and analyze environmental data.',
            'department_id': dept.id,
            'group_leader': 'Meera Desai',
            'members': 'Meera Desai, Jay Mehta, Ravi Sharma, Anjali Patel',
            'marks': None
        },
        {
            'name': 'Student Attendance App',
            'description': 'Mobile application for tracking student attendance using biometric authentication.',
            'department_id': dept.id,
            'group_leader': 'Kunal Shah',
            'members': 'Kunal Shah, Pooja Patel, Rohan Joshi, Sneha Kumar',
            'marks': None
        },
        {
            'name': 'College Event Portal',
            'description': 'Web portal for managing college events, registrations, and generating attendance certificates.',
            'department_id': dept.id,
            'group_leader': 'Anita Desai',
            'members': 'Anita Desai, Rahul Patel, Kiran Shah, Maya Singh',
            'marks': None
        },
        {
            'name': 'Lab Equipment Tracker',
            'description': 'System to track and manage laboratory equipment, maintenance schedules, and usage logs.',
            'department_id': dept.id,
            'group_leader': 'Vikram Mehta',
            'members': 'Vikram Mehta, Nisha Patel, Arun Kumar, Divya Shah',
            'marks': None
        }
    ]

    # Add projects to database
    for project_data in projects:
        project = Project.query.filter_by(name=project_data['name']).first()
        if not project:
            project = Project(**project_data)
            db.session.add(project)
    
    db.session.commit()
    print("Sample projects added successfully!")
