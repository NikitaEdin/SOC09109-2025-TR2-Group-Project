from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, SelectField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional

# Step 1: Get location of the project
class ProjectLocation(FlaskForm):
    longitude = FloatField('Longitude',validators=[DataRequired()])
    altitude = FloatField('Altitude',validators=[DataRequired()])
    submit = SubmitField('Next')


# Step 2: Get project type
class ProjectType(FlaskForm):
    projectType = SelectField('Project Type', choices=[('Rural', 'Rural'), ('Urban', 'Urban')], validators=[DataRequired()])
    submit = SubmitField('Next')

# Step 3: Get the required project details
class ProjectDetails(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    dateOfFlight = DateField('Date of Flight')

    submit = SubmitField('Create Project')

