from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, validators
from wtforms.validators import DataRequired, Email, Length, EqualTo
from app.models import Role
from app.utils.validators import validate_password

class addUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=18)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[
        DataRequired(), 
        validate_password,  
        validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    role_id = SelectField("Role", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Add User")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role_id.choices = [(role.id, role.title) for role in Role.query.all()]