from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, FileField, FieldList, FormField, IntegerField
from wtforms.validators import DataRequired, Optional

class ItemRequestForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    estimated_cost = FloatField('Estimated Cost (₹)', validators=[DataRequired()])
    quotations = FileField('Upload Quotations', validators=[DataRequired()])

class FundRequestForm(FlaskForm):
    project_title = StringField('Project Title', validators=[DataRequired()])
    application_number = StringField('Application Number', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    team_leader = StringField('Team Leader Name', validators=[DataRequired()])
    items = FieldList(FormField(ItemRequestForm), min_entries=1)
    purpose = TextAreaField('Purpose of Purchase', validators=[DataRequired()])
    mentor_name = StringField('Faculty Mentor Name', validators=[DataRequired()])
    mentor_signature = FileField('Faculty Mentor Signature', validators=[DataRequired()])

class ItemUtilizationForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    cost = FloatField('Cost (₹)', validators=[DataRequired()])
    invoice = FileField('Upload Invoice', validators=[DataRequired()])

class UtilizationForm(FlaskForm):
    project_title = StringField('Project Title', validators=[DataRequired()])
    application_number = StringField('Application Number', validators=[DataRequired()])
    total_sanctioned = FloatField('Total Grant Sanctioned (₹)', validators=[DataRequired()])
    total_utilized = FloatField('Total Amount Utilized (₹)', validators=[DataRequired()])
    items = FieldList(FormField(ItemUtilizationForm), min_entries=1)
    team_leader_signature = FileField('Team Leader Signature', validators=[DataRequired()])
    mentor_signature = FileField('Faculty Mentor Signature', validators=[DataRequired()])
    dept_coordinator_signature = FileField('Department SSIP Coordinator Signature', validators=[DataRequired()])
    finance_member_signature = FileField('SSIP Finance Member Signature', validators=[Optional()])
