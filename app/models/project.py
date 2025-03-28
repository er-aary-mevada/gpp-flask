from app import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id', name='fk_project_department'))
    group_leader = db.Column(db.String(100), nullable=False)
    members = db.Column(db.Text, nullable=False)  # Comma-separated list of members
    marks = db.Column(db.Integer)  # Out of 100
    presentation_type = db.Column(db.String(50))  # Model/Poster
    semester = db.Column(db.String(20))
    faculty_mentor = db.Column(db.String(100))
    mobile_number = db.Column(db.String(15))
    submission_timestamp = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    department = db.relationship('Department', backref=db.backref('projects', lazy=True))

    def __repr__(self):
        return f'<Project {self.name}>'

    @staticmethod
    def import_from_csv(file_path):
        """Import projects from a Google Form responses CSV file"""
        import pandas as pd
        from datetime import datetime
        
        df = pd.read_csv(file_path)
        projects = []
        
        # Column mapping from Google Form to our model
        column_mapping = {
            'Timestamp': 'submission_timestamp',
            'Project Title': 'name',
            'Write about your Idea/project ': 'description',  
            'Demo Model  / Poster ': 'presentation_type',  
            'Select Branch ': 'department',  
            'Select Semester': 'semester',
            'First team member name  (for certificate printing)': 'group_leader',
            'Mobile number any one team member': 'mobile_number',
            'Faculty Mentor Name': 'faculty_mentor'
        }
        
        member_columns = [
            'First team member name  (for certificate printing)',
            'Second team member name  (for certificate printing)',
            'Third team member name  (for certificate printing)',
            'Forth team member name  (for certificate printing)',
            'Fifth team member name  (for certificate printing)'
        ]
        
        for _, row in df.iterrows():
            # Get department ID (create if doesn't exist)
            from app.models.department import Department
            dept_name = row['Select Branch '].strip()
            dept = Department.query.filter_by(name=dept_name).first()
            if not dept:
                dept = Department(name=dept_name)
                db.session.add(dept)
                db.session.commit()
            
            # Combine team members, filtering out empty entries
            members = [row[col].strip() for col in member_columns if pd.notna(row[col]) and row[col].strip()]
            members_str = ', '.join(members)
            
            # Parse timestamp
            timestamp = datetime.strptime(row['Timestamp'], '%m/%d/%Y %H:%M:%S')
            
            project = Project(
                name=row['Project Title'].strip(),
                description=row['Write about your Idea/project '].strip(),  
                department_id=dept.id,
                group_leader=row['First team member name  (for certificate printing)'].strip(),
                members=members_str,
                presentation_type=row['Demo Model  / Poster '].strip(),  
                semester=row['Select Semester'].strip(),
                faculty_mentor=row['Faculty Mentor Name'].strip(),
                mobile_number=str(row['Mobile number any one team member']),
                submission_timestamp=timestamp,
                marks=None
            )
            projects.append(project)
        
        return projects
