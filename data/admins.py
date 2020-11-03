import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Admin(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'admins'
    userid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

