import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from .favorites import Favorites
from .upvotes import Upvotes


class Tracks(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Tracks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    genres = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    track_file = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    author = None

    # user = orm.relationship('User')
    # comments = orm.relationship("Comments")

    def __repr__(self):
        return f'{self.id}, {self.name}, {self.genres}, {self.author}, {self.description},' \
               f' {self.image}, {self.track_file}'

    def set_rating(self, users: Upvotes):
        self.rating = len(users)
        self.upvoted_users = [user.user_id for user in users]

    def set_favorite_users(self, users: Favorites):
        self.favorite_users = [user.user_id for user in users]
