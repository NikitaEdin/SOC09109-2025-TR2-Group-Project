from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, ValidationError, Optional

class ViabilityStudyForm(FlaskForm):

    flightCode = StringField('Flight Code:', validators=[DataRequired()])
    summary = TextAreaField('Summary:', validators=[DataRequired()])
    flightDate = DateField('Flight Date:', format='%Y-%m-%d', validators=[DataRequired()])
    preparedBy = StringField('Prepared By:', validators=[DataRequired()])
    preparedDate = DateField('Prepared Date:', format='%Y-%m-%d', validators=[DataRequired()])
    airSpaceClass = StringField('Air Space Class:', validators=[DataRequired()])
    airspaceObservations = TextAreaField('Observations:', validators=[DataRequired()])
    airspaceSources = TextAreaField('Sources:', validators=[DataRequired()])
    groundObservations = TextAreaField('Observations:', validators=[DataRequired()])
    groundSources = TextAreaField('Sources:', validators=[DataRequired()])
    weatherObservations = TextAreaField('Observations:', validators=[DataRequired()])
    weatherSources = TextAreaField('Sources:', validators=[DataRequired()])


    submit = SubmitField('Submit')
    saveChanges = SubmitField('Save Changes')