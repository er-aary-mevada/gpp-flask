from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from ..models.department import Department

class UserCreationForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    department = SelectField('Department', coerce=int, validators=[DataRequired()])
    role = SelectField('Role', choices=[
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('lab_assistant', 'Lab Assistant'),
        ('hod', 'HOD'),
        ('librarian', 'Librarian'),
        ('principal', 'Principal'),
        ('store_officer', 'Store Officer')
    ], validators=[DataRequired()])
    submit = SubmitField('Create User')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.department.choices = [(0, 'Select Department')] + [
            (dept.id, dept.name) for dept in Department.query.order_by('name')
        ]

class BulkUserUploadForm(FlaskForm):
    file = FileField('CSV File', validators=[
        DataRequired(),
        FileAllowed(['csv'], 'CSV files only!')
    ])
    role = SelectField('Role for All Users', choices=[
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('lab_assistant', 'Lab Assistant'),
        ('hod', 'HOD'),
        ('librarian', 'Librarian'),
        ('principal', 'Principal'),
        ('store_officer', 'Store Officer')
    ], validators=[DataRequired()])
    submit = SubmitField('Upload and Create Users')
