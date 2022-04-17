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
    category = RadioField('Category', choices=[("1", "Верхняя одежда"), ("2", "Штаны, шорты, юбки"),
                                               ("3", "Платья"), ("4", "Украшения"), ("5", "Обувь"),
                                               ("6", "Очки, сумки"), ("7", "Футболки, майки"),
                                               ("8", "Свитера, худи"), ("9", "Шапки, кепки, платки")])
    size = StringField('Size')
    price = StringField('Price')
    photo = FileField('Photo')
    submit = SubmitField('Add product')
