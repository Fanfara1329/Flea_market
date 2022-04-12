from orm.users import User
from flask import Flask, render_template, request
from orm import db_session
import forms

app = Flask(__name__)
db_session.global_init("db/flea.db")
app.config['SECRET_KEY'] = 'блаблабла'


@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        print(90)

    elif request.method == 'POST':
        print(45)
        user = User(name=form.name.data,
                    email=form.email.data,
                    city=form.city.data,
                    cards=form.cards.data,
                    password=form.password.data,
                    gender=form.gender.data)
        s = db_session.create_session()
        s.add(user)
        s.commit()
        s.close()
        return "Отправлена"
    return render_template('index.html', form=form)


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
        s.add(user)
        s.commit()
        s.close()
        return "Отправлена"
    return render_template('registration.html', title='Registration', form=form)

db_sess = db_session.create_session()
db_sess.commit()


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
