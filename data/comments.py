import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


# TODO: connect it to tracks
class Comments(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Comments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    track_id = sqlalchemy.Column(sqlalchemy.Integer)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # user = orm.relationship('User')
    # track_id = orm.relationship("Tracks")

    def __repr__(self):
        return [self.id, self.author_id, self.content]
