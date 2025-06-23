from datetime import datetime
from app.extensions import db

class FeePayment(db.Model):
    __tablename__ = 'fee_payments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    fee_type = db.Column(db.String(50), nullable=False)  # e.g., 'tuition', 'hostel', 'exam'
    semester = db.Column(db.Integer)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), default='pending')  # pending, success, failed
    payment_mode = db.Column(db.String(20))  # online, cash, etc.
    
    student = db.relationship('User', backref=db.backref('fee_payments', lazy=True))

class DocumentRequest(db.Model):
    __tablename__ = 'document_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)  # e.g., 'bonafide', 'transcript'
    purpose = db.Column(db.Text)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, ready
    issued_date = db.Column(db.DateTime)
    issued_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    document_file = db.Column(db.String(255))  # path to uploaded document if any
    
    student = db.relationship('User', foreign_keys=[student_id], backref=db.backref('document_requests', lazy=True))
    issued_by = db.relationship('User', foreign_keys=[issued_by_id])

class Grievance(db.Model):
    __tablename__ = 'grievances'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # academic, hostel, ragging, etc.
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='submitted')  # submitted, in_progress, resolved, rejected
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    resolution = db.Column(db.Text)
    resolution_date = db.Column(db.DateTime)
    is_anonymous = db.Column(db.Boolean, default=False)
    
    student = db.relationship('User', foreign_keys=[student_id], backref=db.backref('grievances', lazy=True))
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id])

class PlacementApplication(db.Model):
    __tablename__ = 'placement_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='applied')  # applied, shortlisted, interviewed, selected, rejected
    resume = db.Column(db.String(255))  # path to resume file
    cover_letter = db.Column(db.Text)
    interview_date = db.Column(db.DateTime)
    remarks = db.Column(db.Text)
    
    student = db.relationship('User', backref=db.backref('placement_applications', lazy=True))

class JobPosting(db.Model):
    __tablename__ = 'job_postings'
    
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    salary_range = db.Column(db.String(50))
    posting_date = db.Column(db.DateTime, default=datetime.utcnow)
    application_deadline = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    eligible_departments = db.Column(db.String(255))  # comma-separated department IDs
    required_cgpa = db.Column(db.Float)
    job_location = db.Column(db.String(100))
    job_type = db.Column(db.String(50))  # full-time, internship, etc.
