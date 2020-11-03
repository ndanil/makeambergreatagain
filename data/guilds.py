import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Guild(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'guilds'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    tag = sqlalchemy.Column(sqlalchemy.String, unique=True)
