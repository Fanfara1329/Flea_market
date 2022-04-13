from orm.users import User
from flask import Flask, render_template, request, redirect
from orm import db_session
import forms
from flask_login import LoginForm, LoginManager, current_user, login_user

app = Flask(__name__)
db_session.global_init("db/flea.db")
app.config['SECRET_KEY'] = 'блаблабла'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        print(90)

    elif request.method == 'POST':
        print(45)
        user = User(email=form.email.data,
                    password=form.password.data)
        s = db_session.create_session()
        s.add(user)
        s.commit()
        s.close()
        return "Отправлена"
    return render_template('index.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    format = LoginForm()
    if format.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == format.email.data).first()
        if user and user.check_password(format.password.data):
            login_user(user, remember=format.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=format)
    return render_template('login.html', title='Авторизация', form=format)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        print(90)

    elif request.method == 'POST':
        user = User(name=form.name.data,
                    email=form.email.data,
                    city=form.city.data,
                    cards=form.cards.data,
                    password=form.password.data,
                    gender=form.gender.data)
        s = db_session.create_session()
        try:
            s.add(user)
            s.commit()
            return render_template('user-orders.html', name=form.name.data)
        except IndexError:
            return "хуй"
        except Exception as e:
            print(e)
        finally:
            s.close()
    return render_template('registration.html', title='Registration', form=form)


db_sess = db_session.create_session()
db_sess.commit()


@app.route('/like')
def like():
    return render_template('like.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
