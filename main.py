from orm.users import User
from orm import db_session
from flask import Flask

app = Flask(__name__)
db_session.global_init("db/flea.db")
app.config['SECRET_KEY'] = 'abobys'

user2 = User()
user2.id = 221133311331
user2.name = "Полedfsfьзовwffатель 1"
user2.city = "qeewffwf"
user2.password = "1wfwfwww2f"
user2.cards = "12hwffwswwffeffjskjf"
user2.gender = "mawfffwwswdle"
user2.email = "emaiwfwfwl@eefefefeefmail.ru"

db_sess = db_session.create_session()
db_sess.add(user2)
db_sess.commit()