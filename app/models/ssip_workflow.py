from ..extensions import db
from datetime import datetime

class SSIPWorkflow(db.Model):
    __tablename__ = 'ssip_workflows'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('ssip_submissions.id'), nullable=False)
    
    # Who approved/rejected
    dept_coordinator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    college_coordinator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    principal_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # When they approved/rejected
    dept_action_date = db.Column(db.DateTime)
    college_action_date = db.Column(db.DateTime)
    principal_action_date = db.Column(db.DateTime)
    
    # Their remarks
    dept_remarks = db.Column(db.Text)
    college_remarks = db.Column(db.Text)
    principal_remarks = db.Column(db.Text)
    
    # Their decisions
    dept_status = db.Column(db.String(20))  # approved/rejected
    college_status = db.Column(db.String(20))  # approved/rejected
    principal_status = db.Column(db.String(20))  # approved/rejected
    
    # Current state
    current_reviewer = db.Column(db.String(50), default='department')  # department/college/principal
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    submission = db.relationship('SSIPSubmission', back_populates='workflow')
    dept_coordinator = db.relationship('User', foreign_keys=[dept_coordinator_id])
    college_coordinator = db.relationship('User', foreign_keys=[college_coordinator_id])
    principal = db.relationship('User', foreign_keys=[principal_id])
