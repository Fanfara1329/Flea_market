from orm.users import User
from orm.products import Product
from flask import Flask, render_template, request, redirect
from orm import db_session
import forms
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


@app.route('/', methods=['POST', 'GET'])
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
    print(current_user.is_anonymous)
    return render_template('index.html', form=form, auth=True)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    email=form.email.data,
                    city=form.city.data,
                    cards=form.cards.data,
                    gender=form.gender.data,
                    likes_products='')
        user.set_password(form.password.data)
        s = db_session.create_session()
        s.add(user)
        s.commit()
        s.close()

    return render_template('index.html', title='Registration', auth=False, form=form)


@app.route('/like')
def like():
    return render_template('like.html')


@app.route('/person', methods=['POST', 'GET'])
def person():
    return render_template('person.html')


@app.route('/product', methods=['POST', 'GET'])
def new_product():
    prod = []
    db_session.global_init("db/flea.db")
    db_sess = db_session.create_session()
    for user in db_sess.query(Product).filter(Product.ven_id == current_user.id):
        prod.append(user)
    if len(prod) == 0:
        return render_template('nope.html')
    else:
        pro = db_sess.query(Product).filter(Product.ven_id == current_user.id)
        return render_template("conclusion.html", products=pro)


@app.route('/new', methods=['POST', 'GET'])
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


@app.route('/box')
def box():
    return render_template('box.html')


@app.route('/user-account')
def data():
    return render_template('data.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


db_sess = db_session.create_session()
db_sess.commit()

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
