from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField, BooleanField, FileField
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


class NewProductForm(FlaskForm):
    name = StringField('Name product')
    describe = StringField('Describe')
    category = RadioField('Category', choices=[('1', ''), ('2', '')])
    size = StringField('Size')
    price = StringField('Price')
    photo = FileField('Photo')
    submit = SubmitField('Add product')
