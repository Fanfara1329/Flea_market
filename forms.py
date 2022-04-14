from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField, BooleanField
from wtforms.validators import Email, DataRequired, EqualTo, NumberRange


class RegistrationForm(FlaskForm):
    email = StringField('E-mail')
    name = StringField('Name')
    city = StringField('City')
    password = PasswordField('Password')
    check_password = PasswordField('Repeat password ')
    gender = RadioField('Gender', choices=[('m', 'male'), ('f', 'female')])
    cards = StringField('Card')
    submit = SubmitField('Registration')


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField(' ')
    submit = SubmitField('Войти')
