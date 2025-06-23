from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, TextAreaField, FileField, BooleanField
from wtforms.validators import DataRequired, Optional, Length, NumberRange, Email
from flask_wtf.file import FileAllowed

class FeePaymentForm(FlaskForm):
    fee_type = SelectField('Fee Type', choices=[
        ('tuition', 'Tuition Fee'),
        ('hostel', 'Hostel Fee'),
        ('exam', 'Examination Fee'),
        ('other', 'Other Fee')
    ], validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    semester = IntegerField('Semester', validators=[DataRequired(), NumberRange(min=1, max=8)])

class DocumentRequestForm(FlaskForm):
    document_type = SelectField('Document Type', choices=[
        ('bonafide', 'Bonafide Certificate'),
        ('transcript', 'Transcript'),
        ('character', 'Character Certificate'),
        ('migration', 'Migration Certificate'),
        ('other', 'Other Document')
    ], validators=[DataRequired()])
    purpose = TextAreaField('Purpose', validators=[DataRequired(), Length(min=10, max=500)])
    additional_info = TextAreaField('Additional Information', validators=[Optional(), Length(max=500)])

class GrievanceForm(FlaskForm):
    category = SelectField('Category', choices=[
        ('academic', 'Academic Issues'),
        ('hostel', 'Hostel Issues'),
        ('ragging', 'Ragging Related'),
        ('facilities', 'Institute Facilities'),
        ('other', 'Other Issues')
    ], validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=20, max=2000)])
    is_anonymous = BooleanField('Submit Anonymously')
    attachment = FileField('Attachment (Optional)', validators=[
        Optional(),
        FileAllowed(['pdf', 'jpg', 'png'], 'Only PDF and images are allowed!')
    ])

class PlacementApplicationForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    resume = FileField('Resume', validators=[
        DataRequired(),
        FileAllowed(['pdf'], 'Only PDF files are allowed!')
    ])
    cover_letter = TextAreaField('Cover Letter', validators=[Optional(), Length(max=2000)])

class JobPostingForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    description = TextAreaField('Job Description', validators=[DataRequired(), Length(min=50)])
    requirements = TextAreaField('Requirements', validators=[DataRequired()])
    salary_range = StringField('Salary Range', validators=[Optional()])
    application_deadline = StringField('Application Deadline', validators=[DataRequired()])
    job_location = StringField('Job Location', validators=[DataRequired()])
    job_type = SelectField('Job Type', choices=[
        ('full-time', 'Full Time'),
        ('internship', 'Internship'),
        ('part-time', 'Part Time')
    ], validators=[DataRequired()])
    required_cgpa = FloatField('Required CGPA', validators=[Optional(), NumberRange(min=0, max=10)])
    eligible_departments = SelectField('Eligible Departments', choices=[], validators=[DataRequired()])
