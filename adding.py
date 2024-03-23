from data.users import User
from data import db_session


def main():
    user = User()
    user.name = "Пользователь 1"
    user.display_name = "пользз"
    user.email = "email1@email.ru"
    user.set_password("123")
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


if __name__ == '__main__':
    db_session.global_init('db/blogs.db')
    main()
