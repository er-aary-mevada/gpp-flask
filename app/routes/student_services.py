from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.models.student_services import (
    FeePayment, DocumentRequest, Grievance, PlacementApplication, JobPosting
)
from app.forms.student_services import (
    FeePaymentForm, DocumentRequestForm, GrievanceForm, 
    PlacementApplicationForm, JobPostingForm
)
from app.extensions import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime

bp = Blueprint('student_services', __name__, url_prefix='/student-services')

@bp.route('/')
@login_required
def index():
    """Student Services Dashboard"""
    return render_template('student_services/index.html', title='Student Services')

# Fee Payment Routes
@bp.route('/fee-payment', methods=['GET', 'POST'])
@login_required
def fee_payment():
    form = FeePaymentForm()
    if form.validate_on_submit():
        payment = FeePayment(
            student_id=current_user.id,
            amount=form.amount.data,
            fee_type=form.fee_type.data,
            semester=form.semester.data,
            payment_mode='online',  # Always online payment
            status='pending'
        )
        db.session.add(payment)
        db.session.commit()
        
        # Here you would integrate with a payment gateway
        # For now, we'll just show a success message
        flash('Fee payment initiated successfully!', 'success')
        return redirect(url_for('student_services.fee_payment_history'))
    
    return render_template('student_services/fee_payment.html', form=form)

@bp.route('/fee-payment-history')
@login_required
def fee_payment_history():
    payments = FeePayment.query.filter_by(student_id=current_user.id)\
        .order_by(FeePayment.payment_date.desc()).all()
    return render_template('student_services/fee_payment_history.html', payments=payments)

# Document Request Routes
@bp.route('/document-request', methods=['GET', 'POST'])
@login_required
def document_request():
    form = DocumentRequestForm()
    if form.validate_on_submit():
        request_doc = DocumentRequest(
            student_id=current_user.id,
            document_type=form.document_type.data,
            purpose=form.purpose.data
        )
        db.session.add(request_doc)
        db.session.commit()
        flash('Document request submitted successfully!', 'success')
        return redirect(url_for('student_services.document_request_history'))
    
    return render_template('student_services/document_request.html', form=form)

@bp.route('/document-request-history')
@login_required
def document_request_history():
    requests = DocumentRequest.query.filter_by(student_id=current_user.id)\
        .order_by(DocumentRequest.request_date.desc()).all()
    return render_template('student_services/document_request_history.html', requests=requests)

# Grievance Routes
@bp.route('/grievance', methods=['GET', 'POST'])
@login_required
def grievance():
    form = GrievanceForm()
    if form.validate_on_submit():
        grievance = Grievance(
            student_id=current_user.id,
            category=form.category.data,
            subject=form.subject.data,
            description=form.description.data,
            is_anonymous=form.is_anonymous.data
        )
        
        if form.attachment.data:
            file = form.attachment.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'grievances', filename))
            grievance.attachment = filename
            
        db.session.add(grievance)
        db.session.commit()
        flash('Your grievance has been submitted successfully!', 'success')
        return redirect(url_for('student_services.grievance_history'))
    
    return render_template('student_services/grievance.html', form=form)

@bp.route('/grievance-history')
@login_required
def grievance_history():
    grievances = Grievance.query.filter_by(student_id=current_user.id)\
        .order_by(Grievance.submission_date.desc()).all()
    return render_template('student_services/grievance_history.html', grievances=grievances)

# Training and Placement Routes
@bp.route('/job-postings')
@login_required
def job_postings():
    # Get job postings relevant to student's department
    postings = JobPosting.query.filter(
        JobPosting.is_active == True,
        JobPosting.application_deadline > datetime.utcnow()
    ).order_by(JobPosting.posting_date.desc()).all()
    
    return render_template('student_services/job_postings.html', postings=postings)

@bp.route('/apply-job/<int:posting_id>', methods=['GET', 'POST'])
@login_required
def apply_job(posting_id):
    posting = JobPosting.query.get_or_404(posting_id)
    form = PlacementApplicationForm()
    
    if form.validate_on_submit():
        # Save resume file
        resume = form.resume.data
        resume_filename = secure_filename(f"{current_user.id}_{posting_id}_{resume.filename}")
        resume.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'resumes', resume_filename))
        
        application = PlacementApplication(
            student_id=current_user.id,
            company_name=posting.company_name,
            position=posting.position,
            resume=resume_filename,
            cover_letter=form.cover_letter.data
        )
        
        db.session.add(application)
        db.session.commit()
        flash('Your application has been submitted successfully!', 'success')
        return redirect(url_for('student_services.application_history'))
    
    return render_template('student_services/apply_job.html', form=form, posting=posting)

@bp.route('/application-history')
@login_required
def application_history():
    applications = PlacementApplication.query.filter_by(student_id=current_user.id)\
        .order_by(PlacementApplication.application_date.desc()).all()
    return render_template('student_services/application_history.html', applications=applications)
