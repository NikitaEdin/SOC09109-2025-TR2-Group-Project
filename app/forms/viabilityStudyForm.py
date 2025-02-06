from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, ValidationError, Optional

class ViabilityStudyForm(FlaskForm):

    flightCode = StringField('Flight Code', validators=[DataRequired()])
    summary = TextAreaField('Summary', validators=[DataRequired()])
    flightDate = DateField('Flight Date', format='%Y-%m-%d', validators=[DataRequired()])
    preparedBy = StringField('Prepared By', validators=[DataRequired()])
    preparedDate = DateField('Prepared Date', format='%Y-%m-%d', validators=[DataRequired()])
    airSpaceClass = StringField('Air Space Class', validators=[DataRequired()])
    airspaceObservations = StringField('Airspace Observations', validators=[DataRequired()])
    airspaceSources = StringField('Airspace Sources', validators=[DataRequired()])
    groundObservations = StringField('Ground Observations', validators=[DataRequired()])
    groundSources = StringField('Ground Sources', validators=[DataRequired()])
    weatherObservations = StringField('Weather Observations', validators=[DataRequired()])
    weatherSources = StringField('Weather Sources', validators=[DataRequired()])


    submit = SubmitField('Submit')
    saveChanges = SubmitField('Save Changes')