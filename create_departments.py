from app import create_app
from app.extensions import db
from app.models.department import Department

app = create_app()

departments = [
    "Computer Science",
    "Electronics",
    "Mechanical",
    "Civil",
    "Electrical",
    "Information Technology",
    "Chemical",
    "Automobile"
]

with app.app_context():
    for dept_name in departments:
        if not Department.query.filter_by(name=dept_name).first():
            department = Department(name=dept_name)
            db.session.add(department)
            print(f"Added department: {dept_name}")
    
    db.session.commit()
    print("\nAll departments created successfully!")
