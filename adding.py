from data.comments import Comments
from data import db_session



def main():
    comment = Comments()
    comment.author_id = 1
    comment.content = 'very good, but could be better'
    db_sess = db_session.create_session()
    db_sess.add(comment)
    db_sess.commit()


if __name__ == '__main__':
    db_session.global_init('db/blogs.db')
    main()
