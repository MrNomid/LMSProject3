from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    content = StringField('Написать', validators=[DataRequired()])
    submit = SubmitField('Отправить')
