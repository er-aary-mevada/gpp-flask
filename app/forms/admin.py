from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email, ValidationError, Length
from ..models.department import Department
from ..models.user import Role

class UserCreationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    roles = SelectMultipleField('Roles', validators=[DataRequired()])
    department = SelectField('Department', validators=[DataRequired()])
    submit = SubmitField('Create User')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.department.choices = [(str(d.id), d.name) for d in Department.query.all()]
        self.roles.choices = [(role.name, role.name.title()) for role in Role.query.all()]

class UserEditForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    roles = SelectMultipleField('Roles', validators=[DataRequired()])
    department = SelectField('Department', validators=[DataRequired()])
    submit = SubmitField('Update User')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.department.choices = [(str(d.id), d.name) for d in Department.query.all()]

class BulkUserUploadForm(FlaskForm):
    csv_file = FileField('CSV File', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'CSV files only!')
    ])
    default_roles = SelectMultipleField('Default Roles')
    submit = SubmitField('Upload Users')
    
    def __init__(self, *args, **kwargs):
        super(BulkUserUploadForm, self).__init__(*args, **kwargs)
        self.default_roles.choices = [(role.name, role.name.title()) for role in Role.query.all()]

class ResultUploadForm(FlaskForm):
    result_file = FileField('Result File (CSV)', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'CSV files only!')
    ])
    submit = SubmitField('Upload Results')
