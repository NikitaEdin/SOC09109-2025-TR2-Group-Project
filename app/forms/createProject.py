from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, SelectField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional

from app.models import ProjectPurpose

# Step 1: Get location of the project
class ProjectLocation(FlaskForm):
    longitude = FloatField('Longitude',validators=[DataRequired()])
    latitude = FloatField('Latitude',validators=[DataRequired()])
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
    projectPurposeID = SelectField("Project Purpose", coerce=int, validators=[DataRequired()])

    submit = SubmitField('Next')

    def __init__(self, *args, **kwargs):
        super(ProjectDetails, self).__init__(*args, **kwargs)
        self.projectPurposeID.choices = [(0, "Select Purpose")] + [
            (purpose.id, purpose.title) for purpose in ProjectPurpose.query.all()
    ]

class ProjectToggles(FlaskForm):
    loadingListRequired = BooleanField('Will we need a loading list?')
    protectedAreaFlight = BooleanField('Are we planning to fly in a protected area?')
    notamRequired = BooleanField('Will we need to submit a NOTAM?')
    leafletDropRequired = BooleanField('Will we need a leaflet drop?')
    localClubNearby = BooleanField('Is there a local club nearby?')
    permissionRequired = BooleanField('Do we need to obtain permission?')

    submit = SubmitField('Create Project')



class EditProject(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
   
    submit = SubmitField('Update Project')
