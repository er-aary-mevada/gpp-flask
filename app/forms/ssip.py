from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, IntegerField, SelectField, 
    FloatField, FileField, FieldList
)
from wtforms.validators import DataRequired, Email, Length, NumberRange

class SSIPSubmissionForm(FlaskForm):
    # Basic Information
    project_title = StringField('Project Title', validators=[DataRequired(), Length(max=200)])
    team_name = StringField('Team Name', validators=[Length(max=100)])
    
    # Team Details
    student_name = StringField('Student Name', validators=[DataRequired(), Length(max=100)])
    enrollment_number = StringField('Enrollment Number', validators=[DataRequired(), Length(max=20)])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(max=15)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    department_id = SelectField('Department', coerce=int, validators=[DataRequired()])
    semester = IntegerField('Semester', validators=[DataRequired(), NumberRange(min=1, max=8)])
    
    # Project Details
    problem_statement = TextAreaField('Problem Statement', validators=[DataRequired()])
    solution_description = TextAreaField('Solution Description', validators=[DataRequired()])
    innovation_description = TextAreaField('Innovation Description')
    technical_description = TextAreaField('Technical Description')
    project_category = SelectField('Project Category', 
        choices=[('', 'Select Category'), ('Hardware', 'Hardware'), ('Software', 'Software'), ('Both', 'Both')],
        validators=[DataRequired()]
    )
    
    # Financial Details
    estimated_project_cost = FloatField('Estimated Project Cost')
    fund_requirement_description = TextAreaField('Fund Requirement Description')
    
    # Additional Information
    current_stage = SelectField('Current Stage',
        choices=[
            ('', 'Select Stage'),
            ('Ideation', 'Ideation'),
            ('PoC', 'Proof of Concept'),
            ('Prototype', 'Prototype'),
            ('MVP', 'Minimum Viable Product')
        ],
        validators=[DataRequired()]
    )
    completion_time = IntegerField('Expected Completion Time (in months)', 
        validators=[DataRequired(), NumberRange(min=1, max=24)]
    )
    mentor_name = StringField('Mentor Name', validators=[Length(max=100)])
    mentor_designation = StringField('Mentor Designation', validators=[Length(max=100)])
    
    # Team Members
    team_members = FieldList(
        StringField('Team Member Name', validators=[Length(max=100)]),
        min_entries=1,
        max_entries=5
    )
    
    # Supporting Documents
    proposal_document = FileField('Detailed Project Proposal')
    presentation = FileField('Project Presentation')
    additional_documents = FileField('Additional Supporting Documents')
