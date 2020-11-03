import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Battle(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'battles'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    guildid = sqlalchemy.Column(sqlalchemy.Integer)
    battletime = sqlalchemy.Column(sqlalchemy.DateTime)
