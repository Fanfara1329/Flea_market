from orm.users import User
from orm.products import Product
from flask import Flask, render_template, request, redirect
from orm import db_session
import forms
import base64
from flask_login import LoginManager, current_user, login_user, login_required, logout_user

app = Flask(__name__)
db_session.global_init("db/flea.db")
app.config['SECRET_KEY'] = 'блаблабла'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['POST', 'GET'])  # главная страничка, несколько киков и категории, также авторизация
def index():
    form = forms.LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('index.html',
                               message="Неправильный логин или пароль",
                               form=form,
                               auth=True)
    return render_template('index.html', form=form, auth=True)


@app.route('/registration', methods=['POST', 'GET'])  # если в кике нажать зарегистрироваться, попадёшь сюда
def registration():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    email=form.email.data,
                    city=form.city.data,
                    cards=form.cards.data,
                    gender=form.gender.data)
        user.set_password(form.password.data)
        s = db_session.create_session()
        s.add(user)
        s.commit()
        s.close()
        return redirect("/")
    return render_template('index.html', title='Registration', auth=False, form=form)


@app.route('/like', methods=['POST', 'GET'])  # лайкнутые товары, пока он говорит, что нет таких
def like():
    form = forms.LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
    return render_template('like.html', form=form, auth=True)


@app.route('/person',
           methods=['POST', 'GET'])  # личный кабинет, от него наследуются мои товары перс. данные моя корзина
def person():
    return render_template('person.html')


@app.route('/product', methods=['POST', 'GET'])  # мои товары, тут он говорит, есть ли созданные товары или нет
def new_product():
    db_session.global_init("db/flea.db")
    db_sess = db_session.create_session()
    pro = []
    for product in db_sess.query(Product).filter(Product.ven_id == current_user.id):
        pro.append(product)
    if len(pro) == 0:
        return render_template('nope.html')
    else:
        pro = db_sess.query(Product).filter(Product.ven_id == current_user.id)
        return render_template("conclusion.html", products=pro, base64=base64, auth=True)


@app.route('/new', methods=['POST', 'GET'])  # создание товара
def new():
    form = forms.NewProductForm()
    if form.validate_on_submit():
        image_data = request.files[form.photo.name].read()
        product = Product(ven_id=current_user.id,
                          name_product=form.name.data,
                          describe=form.describe.data,
                          category_id=form.category.data,
                          photo=image_data,
                          size=form.size.data,
                          price=form.price.data
                          )
        s = db_session.create_session()
        s.add(product)
        s.commit()
        s.close()
    return render_template('product.html', form=form)


@app.route('/box')  # корзина пока не сделана
def box():
    return render_template('box.html')


@app.route('/user-account')  # персональные данные
def data():
    return render_template('data.html')


@app.route('/logout')  # выход из сессии
@login_required
def logout():
    logout_user()
    return redirect("/")


db_sess = db_session.create_session()
db_sess.commit()

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
