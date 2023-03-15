from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, StringField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    name = StringField(label='', name='movie', validators=[DataRequired()])

    
class ReviewForm(FlaskForm):
    rating = SelectField('Rating', name='rating', choices=['1', '2', '3', '4', '5'])
    review = TextAreaField('Review', name='review', render_kw={'style': 'width: 280px; height: 200px;'})


class UpdateForm(FlaskForm):
    rating = SelectField('Rating', name='rating', choices=['1', '2', '3', '4', '5'])
    review = TextAreaField('Review', name='review', render_kw={'style': 'width: 280px; height: 200px;', 'placeholder': 'leave it empty to keep old review'})
    ranking = SelectField('Ranking', name='ranking',  choices=['1', '2', '3', '4', '5', '7', '8', '9'])