from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, ValidationError, Optional

class CrewCallSheetForm(FlaskForm):
    purpose = TextAreaField('Purpose', validators=[DataRequired()])
    timings = TextAreaField('Timings Description', validators=[DataRequired()])
    siteInfo = TextAreaField('Site Information', description="Copy location and description from site evaluation.", validators=[DataRequired()])
    clothingAndPPE = TextAreaField('Clothing & PPE', validators=[DataRequired()])
    otherEquipment = TextAreaField('Other Equipment', validators=[])
    foodAndDrink = TextAreaField('Food & Drink', validators=[DataRequired()])


    submit = SubmitField('Submit')
    saveChanges = SubmitField('Save Changes')