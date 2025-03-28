from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email, ValidationError
from ..models.department import Department

class UserCreationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    roles = SelectMultipleField('Roles', choices=[
        ('admin', 'Admin'),
        ('user', 'User'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
        ('hod', 'HOD'),
        ('store_officer', 'Store Officer')
    ], validators=[DataRequired()])
    department = SelectField('Department', validators=[DataRequired()])
    submit = SubmitField('Create User')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.department.choices = [(str(d.id), d.name) for d in Department.query.all()]

class UserEditForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    roles = SelectMultipleField('Roles', choices=[
        ('admin', 'Admin'),
        ('user', 'User'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
        ('hod', 'HOD'),
        ('store_officer', 'Store Officer')
    ], validators=[DataRequired()])
    department = SelectField('Department', validators=[DataRequired()])
    submit = SubmitField('Update User')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.department.choices = [(str(d.id), d.name) for d in Department.query.all()]

class BulkUserUploadForm(FlaskForm):
    user_file = FileField('User File (CSV)', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'CSV files only!')
    ])
    roles = SelectMultipleField('Default Roles', choices=[
        ('admin', 'Admin'),
        ('user', 'User'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
        ('hod', 'HOD'),
        ('store_officer', 'Store Officer')
    ], validators=[DataRequired()])
    submit = SubmitField('Upload and Create Users')

class ResultUploadForm(FlaskForm):
    result_file = FileField('Result File (CSV)', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'CSV files only!')
    ])
    submit = SubmitField('Upload Results')
