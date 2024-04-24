from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, StringField, FileField,\
    TextAreaField
from wtforms.validators import DataRequired


class LoadTrackForm(FlaskForm):
    track_name = StringField('Название Трека', validators=[DataRequired()])
    genres = StringField('Жанры', validators=[DataRequired()])
    description = TextAreaField('Описание')
    image = FileField('Загрузить обложку')
    track = FileField('Загрузить трек')
    submit = SubmitField('Опубликовать')
