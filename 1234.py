from orm.users import User
from orm.products import Product
from orm.category import Category
from orm.likes import Likes
from orm.box import Box
from user_api import user_api

from flask import Flask, render_template, request, redirect
from orm import db_session
import forms
import base64
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from password_validator import PasswordValidator

app = Flask(__name__)
db_session.global_init("db/flea.db")
app.config['SECRET_KEY'] = 'блаблабла'
app.register_blueprint(user_api)

login_manager = LoginManager()
login_manager.init_app(app)
db_sess = db_session.create_session()
category = db_sess.query(Category).all()


def validates(password):
    a, b, c, d, e, f, g = PasswordValidator(), PasswordValidator(), PasswordValidator(), PasswordValidator(), \
                          PasswordValidator(), PasswordValidator(), PasswordValidator()
    a.min(8), b.max(30), c.has().uppercase(), d.has().lowercase(), e.has().digits()
    f.has().no().spaces(), g.has().letters()

    if not a.validate(password):
        return 'Need more than 8 characters'
    elif not b.validate(password):
        return 'Too long password'
    elif not e.validate(password):
        return 'Need digits'
    elif not g.validate(password):
        return 'Need letters'
    elif not c.validate(password):
        return 'Need uppercase letters'
    elif not d.validate(password):
        return 'Need capital letters'
    elif not f.validate(password):
        return "Don't use spaces"
    else:
        return None


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
    return render_template('index.html', form=form, auth=True, category=category)


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
        mes = validates(form.password.data)
        if mes is None:
            s = db_session.create_session()
            s.add(user)
            s.commit()
            s.close()
            return redirect("/")
        else:
            return render_template('index.html', title='Registration', auth=False, form=form, category=category,
                                   message=mes)
    return render_template('index.html', title='Registration', auth=False, form=form, category=category)


@app.route('/like', methods=['POST', 'GET'])  # лайкнутые товары, пока он говорит, что нет таких
@login_required
def like():
    db_sess = db_session.create_session()
    form = forms.LoginForm()
    try:
        if form.validate_on_submit():
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
    except Exception as e:
        print(e)
    prod = []

    for i in db_sess.query(Likes).filter(Likes.user_id == current_user.id):
        product = db_sess.query(Product).get(i.product_id)
        prod.append(product)
    print(prod)

    return render_template('like.html', form=form, auth=True, products=prod, base64=base64,
                           category=category)


@app.route('/person',
           methods=['POST', 'GET'])  # личный кабинет, от него наследуются мои товары перс. данные моя корзина
@login_required
def person():
    return render_template('person.html', category=category)


@app.route('/product', methods=['POST', 'GET'])  # мои товары, тут он говорит, есть ли созданные товары или нет
@login_required
def new_product():
    db_session.global_init("db/flea.db")
    db_sess = db_session.create_session()
    pro = []
    if request.args:
        if 'product_id' in request.args:
            box = Box(user_id=current_user.id, product_id=request.args["product_id"])
            s = db_session.create_session()
            li = db_sess.query(Box).filter(Box.user_id == current_user.id).all()
            ids = []

            for i in li:
                ids.append(i.product_id)

            if len(ids) != 0:
                if int(request.args['product_id']) in ids:
                    print('Exist in db')
                else:
                    product = s.query(Product).get(int(request.args['product_id']))
                    product.is_buy = 1
                    s.add(box)
                    s.commit()
                    s.close()
            else:
                product = s.query(Product).get(int(request.args['product_id']))
                product.is_buy = 1
                s.add(box)
                s.commit()
                s.close()

        if 'like_id' in request.args:
            like = Likes(user_id=current_user.id, product_id=request.args["like_id"])
            s = db_session.create_session()
            li = db_sess.query(Likes).filter(Likes.user_id == current_user.id).all()
            ids = []

            for i in li:
                ids.append(i.product_id)

            if len(ids) != 0:
                if int(request.args['like_id']) in ids:
                    print('Exist in db')
                else:
                    product = s.query(Product).get(int(request.args['like_id']))
                    product.is_likes = 1
                    s.add(like)
                    s.commit()
                    s.close()
            else:
                product = s.query(Product).get(int(request.args['like_id']))
                product.is_likes = 1
                s.add(like)
                s.commit()
                s.close()

    for product in db_sess.query(Product).filter(Product.ven_id == current_user.id):
        pro.append(product)
    if len(pro) == 0:
        return render_template('nope.html', category=category)
    else:
        pro = db_sess.query(Product).filter(Product.ven_id == current_user.id)
        if 'product_id' in request.args:
            box = Box(user_id=current_user.id, product_id=request.args["product_id"])
            s = db_session.create_session()
            s.add(box)
            s.commit()
            s.close()
        if 'like_id' in request.args:
            like = Likes(user_id=current_user.id, product_id=request.args["like_id"])
            s = db_session.create_session()
            s.add(like)
            s.commit()
            s.close()
        return render_template("conclusion.html", products=pro, base64=base64, category=category)


@app.route('/new', methods=['POST', 'GET'])  # создание товара
@login_required
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
                          price=form.price.data,
                          is_buy=0, is_likes=0
                          )
        s = db_session.create_session()
        s.add(product)
        s.commit()
        s.close()
    return render_template('product.html', form=form, category=category)


@app.route('/box')  # корзина пока не сделана
@login_required
def box():
    f = int(request.args.get("flag", 0))
    print(f)
    form = forms.LoginForm()

    if f:
        products = db_sess.query(Box).filter(Box.user_id == current_user.id).all()
        for i in products:
            db_sess.delete(i)
            db_sess.commit()

    try:
        if form.validate_on_submit():
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
    except Exception as e:
        print(e)

    prod = []
    for i in db_sess.query(Box).filter(Box.user_id == current_user.id):
        product = db_sess.query(Product).get(i.product_id)
        prod.append(product)

    return render_template('box.html', form=form, auth=True, products=prod, base64=base64,
                           category=category)


@app.route('/user-account')  # персональные данные
@login_required
def data():
    return render_template('data.html', category=category)


@app.route('/logout')  # выход из сессии
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/merchandise/<int:cat>', methods=['POST', 'GET'])
@login_required
def merchandise(cat):
    if request.args:
        if 'product_id' in request.args:
            box = Box(user_id=current_user.id, product_id=request.args["product_id"])
            s = db_session.create_session()
            li = db_sess.query(Box).filter(Box.user_id == current_user.id).all()
            ids = []

            for i in li:
                ids.append(i.product_id)

            if len(ids) != 0:
                if int(request.args['product_id']) in ids:
                    print('Exist in db')
                else:
                    product = s.query(Product).get(int(request.args['product_id']))
                    product.is_buy = 1
                    s.add(box)
                    s.commit()
                    s.close()
            else:
                product = s.query(Product).get(int(request.args['product_id']))
                product.is_buy = 1
                s.add(box)
                s.commit()
                s.close()

        if 'like_id' in request.args:
            like = Likes(user_id=current_user.id, product_id=request.args["like_id"])
            s = db_session.create_session()
            li = db_sess.query(Likes).filter(Likes.user_id == current_user.id).all()
            ids = []

            for i in li:
                ids.append(i.product_id)

            if len(ids) != 0:
                if int(request.args['like_id']) in ids:
                    print('Exist in db')
                else:
                    product = s.query(Product).get(int(request.args['like_id']))
                    product.is_likes = 1
                    s.add(like)
                    s.commit()
                    s.close()
            else:
                product = s.query(Product).get(int(request.args['like_id']))
                product.is_likes = 1
                s.add(like)
                s.commit()
                s.close()

    form = forms.LoginForm()
    try:
        if form.validate_on_submit():
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
    except Exception as e:
        print(e)

    prod = 0
    for p in db_sess.query(Product).filter(Product.category_id == cat):
        prod += 1

    if prod != 0:
        products = db_sess.query(Product).filter(Product.category_id == cat)
        return render_template('merchandise.html', form=form, auth=True, products=products, base64=base64,
                               category=category)
    else:
        return render_template('merchandise.html', form=form, auth=True, products=None, base64=base64,
                               category=category)


db_sess = db_session.create_session()
db_sess.commit()

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
