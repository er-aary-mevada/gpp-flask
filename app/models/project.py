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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    department = db.relationship('Department', backref=db.backref('projects', lazy=True))

    def __repr__(self):
        return f'<Project {self.name}>'

    @staticmethod
    def import_from_csv(file_path):
        """Import projects from a CSV file"""
        import pandas as pd
        
        df = pd.read_csv(file_path)
        projects = []
        
        for _, row in df.iterrows():
            project = Project(
                name=row['name'],
                description=row.get('description', ''),
                department_id=row.get('department_id'),
                group_leader=row.get('group_leader', ''),
                members=row.get('members', ''),
                marks=row.get('marks')
            )
            projects.append(project)
        
        return projects
