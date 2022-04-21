import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Likes(SqlAlchemyBase):
    __tablename__ = 'like'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    product_id = sqlalchemy.Column(sqlalchemy.Integer)
