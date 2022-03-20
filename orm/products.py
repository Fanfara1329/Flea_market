import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))  # id
    name_product = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    describe = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.Integer)
    photo = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    size = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    user = orm.relation("User")
