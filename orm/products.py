import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    ven_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    name_product = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    describe = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("category.id"))
    photo = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    size = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # храним в копейках
    is_buy = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    is_likes = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)

    user = orm.relation('User')
    cat = orm.relation('Category')
