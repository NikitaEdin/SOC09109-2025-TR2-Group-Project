from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField, ValidationError, validators
from wtforms.validators import DataRequired, Email, Optional, Length

from app.models import Role
from app.utils.validators import validate_password

class EditUserDetails(FlaskForm):
    display_name = StringField("Display Name", validators=[Optional(), Length(min=4, max=12)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("New Password", validators=[Optional()])
    submit = SubmitField("Save Changes")

# For Admin usage
class EditUserForm(FlaskForm):
    email = StringField('Email', validators=[Email(), Optional()])
    displayname = StringField('Display Name', validators=[Optional()])
    role_id = SelectField('Role', coerce=int, validators=[Optional()])

    password = PasswordField('New Password', validators=[
        Optional(),
        validate_password,
        validators.EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Repeat Password', validators=[
        Optional(),
        validators.EqualTo('password')
    ])


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Fetch roles from DB
        self.role_id.choices = [(role.id, role.title) for role in Role.query.all()]
