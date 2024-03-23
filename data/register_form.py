from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, StringField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя Пользователя', validators=[DataRequired()])
    displayed_name = StringField('Псевдоним', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_confirmation = PasswordField('Повтор пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
