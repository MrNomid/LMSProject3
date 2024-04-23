import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Upvotes(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Upvotes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    track_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Tracks.id'))

    def __repr__(self):
        return f'{self.id}, {self.user_id}, {self.track_id}'
