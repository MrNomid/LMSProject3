import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Comments(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Comments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user = orm.relationship('User')
    tracks = orm.relationship("Tracks")

    def __repr__(self):
        return f'{self.id} {self.author_id}, {self.content}'
