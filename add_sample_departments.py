from app import create_app
from app.extensions import db
from app.models.department import Department

app = create_app()

with app.app_context():
    # Sample departments
    departments = [
        'Computer Engineering',
        'Mechanical Engineering',
        'Civil Engineering',
        'Electrical Engineering',
        'Chemical Engineering'
    ]
    
    for dept_name in departments:
        dept = Department.query.filter_by(name=dept_name).first()
        if not dept:
            dept = Department(name=dept_name)
            db.session.add(dept)
    
    db.session.commit()
    print("Sample departments added successfully!")
