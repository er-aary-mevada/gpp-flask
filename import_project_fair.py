from app import create_app
from app.extensions import db
from app.models.project import Project

app = create_app()

def import_projects_from_form(csv_file):
    """Import projects from Google Form responses CSV file"""
    with app.app_context():
        try:
            projects = Project.import_from_csv(csv_file)
            for project in projects:
                db.session.add(project)
            db.session.commit()
            print(f"Successfully imported {len(projects)} projects!")
            return True
        except Exception as e:
            print(f"Error importing projects: {str(e)}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python import_project_fair.py <path_to_responses.csv>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    import_projects_from_form(csv_file)
