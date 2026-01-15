from flask import Flask, url_for, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import or_

from data.change_form import ChangeForm
from data.comment_form import CommentForm
from data.comments import Comments
from data.favorites import Favorites
from data.login_form import LoginForm
from data.register_form import RegisterForm
from data.load_track_form import LoadTrackForm
from data.db_session import create_session, global_init
from data.search_form import SearchForm
from data.tracks import Tracks
from data.upvotes import Upvotes
from data.users import User
from werkzeug.utils import secure_filename

import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    db_sess = create_session()
    users = db_sess.query(User).all()
    names = {name.id: (name.name) for name in users}
    return render_template("base.html", names=names, title='MOMusic')


# Вход в систему
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/search")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# Регистрация в системе
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data == form.password_confirmation.data:
            user = User()
            user.name = form.name.data
            user.email = form.email.data
            user.set_password(form.password.data)
            db_sess = create_session()
            db_sess.add(user)
            db_sess.commit()
            login_user(user)
            return redirect('/search')
        return render_template('register.html', message='Что-то не так', form=form)
    return render_template('register.html', title='Регистрация', form=form)


# Выход из системы
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# Профиль пользователя
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    db_sess = create_session()
    user_tracks = len(db_sess.query(Tracks).filter(Tracks.author_id == current_user.id).all())
    favourite_tracks = len([db_sess.query(Tracks).filter(Tracks.id == track_id).first()
              for track_id in [f.track_id for f in db_sess.query(Favorites).filter(Favorites.user_id == current_user.id)
        .all()]])

    return render_template('profile.html', user_tracks=user_tracks, favourite_tracks=favourite_tracks)


@app.route('/change', methods=['GET', 'POST'])
def change():
    form = ChangeForm()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            db_sess = create_session()
            user = db_sess.query(User).filter(User.id == current_user.id).first()
            user.name = form.name.data
            db_sess.add(user)
            db_sess.commit()
            db_sess.close()
            return redirect('/profile')

    return render_template('change.html', form=form)


# Загрузка нового трека
@app.route('/load_track', methods=['GET', 'POST'])
def load_track():
    form = LoadTrackForm()
    if form.validate_on_submit():
        image_filename = secure_filename(form.image.data.filename)
        track_filename = secure_filename(form.track.data.filename)
        form.image.data.save(f'static/track_images/{image_filename}')
        form.track.data.save(f'static/tracks/{track_filename}')

        track = Tracks()
        track.name = form.track_name.data
        track.genres = form.genres.data
        track.description = form.description.data
        track.image = f'../static/track_images/{image_filename}'
        track.track_file = f'../static/tracks/{track_filename}'
        track.author_id = current_user.id
        track.rating = 10
        db_sess = create_session()
        db_sess.add(track)
        db_sess.commit()
        db_sess.close()
        return redirect('/my_tracks')
    return render_template('load_track.html', form=form, title="Публикация трека")


# Просммотр треков
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    db_sess = create_session()
    if form.validate_on_submit():
        users = db_sess.query(User).filter(User.name.like(f'%{form.content.data}%')).all()
        if users:
            tracks = db_sess.query(Tracks).filter(or_(Tracks.name.like(f'%{form.content.data}%'), Tracks.author_id == users[0].id)).all()
        else:
            tracks = db_sess.query(Tracks).filter(Tracks.name.like(f'%{form.content.data}%')).all()
    else:
        tracks = db_sess.query(Tracks).all()

    for track in tracks:
        track.author = db_sess.query(User).filter(User.id == track.author_id).first().name
        track.set_rating(db_sess.query(Upvotes).filter(Upvotes.track_id == track.id).all())
        track.set_favorite_users(db_sess.query(Favorites).filter(Favorites.track_id == track.id).all())
    db_sess.close()
    return render_template('search.html', tracks=tracks, form=form)


# Треки пользователя
@app.route('/my_tracks', methods=['GET', 'POST'])
def my_tracks():
    db_sess = create_session()
    tracks = db_sess.query(Tracks).filter(Tracks.author_id == current_user.id).all()
    for track in tracks:
        track.set_rating(db_sess.query(Upvotes).filter(Upvotes.track_id == track.id).all())
        track.set_favorite_users(db_sess.query(Favorites).filter(Favorites.track_id == track.id).all())
    db_sess.close()
    return render_template('my_tracks.html', tracks=tracks)


# Удалить определённый трек
@app.route('/delete/<track_id>')
def delete(track_id):
    db_sess = create_session()
    x = db_sess.query(Tracks).filter(Tracks.id == track_id).first()

    db_sess.delete(x)
    db_sess.commit()
    db_sess.close()

    return redirect(f'/my_tracks')


# Оценить трек
@app.route('/upvote/<track_id>')
def upvote(track_id):
    db_sess = create_session()
    upvoted_tracks = []
    for users_upvote in db_sess.query(Upvotes).filter(Upvotes.user_id == current_user.id).all():
        upvoted_tracks.append(int(users_upvote.track_id))

    if int(track_id) not in upvoted_tracks:
        upvote = Upvotes()
        upvote.track_id = track_id
        upvote.user_id = current_user.id
        db_sess.add(upvote)

    db_sess.commit()
    db_sess.close()

    return redirect('/search')


# Убрать оценку трека
@app.route('/downvote/<track_id>')
def downvote(track_id):
    db_sess = create_session()
    x = db_sess.query(Upvotes).filter(Upvotes.track_id == track_id, Upvotes.user_id == current_user.id).first()

    db_sess.delete(x)
    db_sess.commit()
    db_sess.close()

    return redirect('/search')


# Прокоментировать трек
@app.route('/comment/<track_id>', methods=['GET', 'POST'])
def comment(track_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comments()
        comment.author_id = current_user.id
        comment.content = form.content.data
        comment.track_id = track_id

        db_sess = create_session()
        db_sess.add(comment)
        db_sess.commit()
        db_sess.close()
        return redirect(f'/comment/{track_id}')

    db_sess = create_session()
    track = db_sess.query(Tracks).filter(Tracks.id == track_id).first()
    track.author = db_sess.query(User).filter(User.id == track.author_id).first().name

    comments = db_sess.query(Comments).filter(Comments.track_id == track_id).all()
    for comment in comments:
        comment.author_id = db_sess.query(User).filter(User.id == comment.author_id).first().name
    db_sess.close()
    return render_template('comments.html', comments=comments, track=track, form=form)


# Треки определённого пользователя
@app.route('/users_tracks/<user_id>')
def users_tracks(user_id):
    db_sess = create_session()

    tracks = db_sess.query(Tracks).filter(Tracks.author_id == user_id).all()

    for track in tracks:
        track.author = db_sess.query(User).filter(User.id == track.author_id).first().name
        track.set_rating(db_sess.query(Upvotes).filter(Upvotes.track_id == track.id).all())
        track.set_favorite_users(db_sess.query(Favorites).filter(Favorites.track_id == track.id).all())
    db_sess.close()
    return render_template('search.html', tracks=tracks, form=None)


# Добавить трек в любимое
@app.route('/add_to_favorites/<track_id>')
def add_to_favorites(track_id):
    favorite = Favorites()
    favorite.track_id = track_id
    favorite.user_id = current_user.id

    db_sess = create_session()
    db_sess.add(favorite)
    db_sess.commit()
    db_sess.close()

    return redirect('/search')


# Удалить трек из любимого
@app.route('/remove_from_favorites/<track_id>')
def remove_from_favorites(track_id):
    db_sess = create_session()
    x = db_sess.query(Favorites).filter(Favorites.track_id == track_id, Favorites.user_id == current_user.id).first()

    db_sess.delete(x)
    db_sess.commit()
    db_sess.close()

    return redirect('/favorites')


# Просмотреть любимое треки
@app.route('/favorites')
def favorites():
    db_sess = create_session()
    tracks = [db_sess.query(Tracks).filter(Tracks.id == track_id).first()
              for track_id in [f.track_id for f in db_sess.query(Favorites).filter(Favorites.user_id == current_user.id)
              .all()]]

    db_sess.close()
    for track in tracks:
        track.author = db_sess.query(User).filter(User.id == track.author_id).first().name
        track.set_rating(db_sess.query(Upvotes).filter(Upvotes.track_id == track.id).all())
        track.set_favorite_users(db_sess.query(Favorites).filter(Favorites.track_id == track.id).all())
    return render_template('search.html', tracks=tracks, form=None)


def main():
    global_init('db/blogs.db')
    if __name__ == '__main__':
        port = int(os.environ.get("PORT", 80))
        app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    main()
