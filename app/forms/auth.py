from flask_security.forms import LoginForm as BaseLoginForm, RegisterForm as BaseRegisterForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_security.utils import verify_password, hash_password
from ..models.department import Department
from ..models.user import User

class ExtendedRegisterForm(BaseRegisterForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    password_confirm = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
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
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super(ExtendedRegisterForm, self).__init__(*args, **kwargs)
        self.department.choices = [(0, 'Select Department')] + [
            (dept.id, dept.name) for dept in Department.query.order_by('name')
        ]

class LoginForm(BaseLoginForm):
    # Add our custom role field to Flask-Security's LoginForm
    role = SelectField('Login As', choices=[
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('lab_assistant', 'Lab Assistant'),
        ('hod', 'HOD'),
        ('librarian', 'Librarian'),
        ('principal', 'Principal'),
        ('store_officer', 'Store Officer'),
        ('admin', 'Administrator')
    ], validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.requires_confirmation = False
        self.user = None

    def validate(self, extra_validators=None):
        # First run Flask-Security's validation
        if not super(LoginForm, self).validate():
            return False

        # Find the user
        self.user = User.query.filter_by(email=self.email.data).first()

        # Check if user exists and password is correct
        if self.user is None or not verify_password(self.password.data, self.user.password):
            self.email.errors.append('Invalid email or password')
            return False

        # Check if user is approved
        if not self.user.is_approved and not self.user.has_role('admin'):
            self.email.errors.append('Your account is pending approval.')
            return False

        # Check if user has the selected role
        if not self.user.has_role(self.role.data):
            self.role.errors.append('You do not have permission to login with this role.')
            return False

        return True
