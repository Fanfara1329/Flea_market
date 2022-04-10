from orm.users import User
from flask import Flask, template_rendered, request, render_template
from orm import db_session
import forms

app = Flask(__name__)
db_session.global_init("db/flea.db")
app.config['SECRET_KEY'] = 'abobys'


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

app.run(port=8080, debug=True)
