import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Tracks(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Tracks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    genres = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    rating = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=1)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    track_file = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    comments = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("comments.id"))

    user = orm.relationship('User')
    comments = orm.relationship("Comments")

    def __repr__(self):
        return f'{self.id}, {self.name}, {self.genres}, {self.author}, {self.description}, {self.rating},' \
               f' {self.image}, {self.track_file}'
