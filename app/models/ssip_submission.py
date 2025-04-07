from datetime import datetime
from ..extensions import db
import random
import string

class SSIPSubmission(db.Model):
    __tablename__ = 'ssip_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Information
    application_number = db.Column(db.String(20), unique=True)
    project_title = db.Column(db.String(200), nullable=False)
    team_name = db.Column(db.String(100))
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def generate_application_number(department_id):
        # Format: SSIP-DEPT-YEAR-RANDOM
        year = datetime.utcnow().strftime('%y')
        random_digits = ''.join(random.choices(string.digits, k=4))
        return f'SSIP-{department_id:02d}-{year}-{random_digits}'
    
    # Team Details
    student_name = db.Column(db.String(100), nullable=False)
    enrollment_number = db.Column(db.String(20), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    semester = db.Column(db.Integer, nullable=False)
    
    # Project Details
    problem_statement = db.Column(db.Text, nullable=False)
    solution_description = db.Column(db.Text, nullable=False)
    innovation_description = db.Column(db.Text)
    technical_description = db.Column(db.Text)
    project_category = db.Column(db.String(50))  # Hardware/Software/Both
    
    # Financial Details
    estimated_project_cost = db.Column(db.Float)
    fund_requirement_description = db.Column(db.Text)
    
    # Additional Information
    current_stage = db.Column(db.String(50))  # Ideation/PoC/Prototype/MVP
    completion_time = db.Column(db.Integer)  # in months
    mentor_name = db.Column(db.String(100))
    mentor_designation = db.Column(db.String(100))
    
    # Team Members (can be multiple)
    team_members = db.Column(db.Text)  # Stored as JSON string
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending/approved/rejected
    remarks = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    department = db.relationship('Department', backref=db.backref('ssip_submissions', lazy=True))
    workflow = db.relationship('SSIPWorkflow', back_populates='submission', uselist=False)
    
    def __repr__(self):
        return f'<SSIPSubmission {self.project_title}>'
