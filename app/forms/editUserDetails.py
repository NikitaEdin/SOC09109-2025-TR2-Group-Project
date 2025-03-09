from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length

class EditUserDetails(FlaskForm):
    display_name = StringField("Display Name", validators=[Optional(), Length(min=4, max=12)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Save Changes")