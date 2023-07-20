from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange


class BookForm(FlaskForm):
    title = StringField(label='Book Title', validators=[DataRequired()])
    author = StringField(label='Author Name', validators=[DataRequired()])
    rating = FloatField(label='Your Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField(label='Submit')
    cancel = SubmitField(label='Cancel')
