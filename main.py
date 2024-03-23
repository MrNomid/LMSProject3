from flask import Flask, url_for, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required

from data.login_form import LoginForm
from data.register_form import RegisterForm
from data.db_session import create_session, global_init
from data.users import User

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(1)
    if form.validate_on_submit():
        print(1)
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            print(2)
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data == form.password_confirmation.data:
            user = User()
            user.name = form.name.data
            user.display_name = form.displayed_name.data
            user.email = form.email.data
            user.set_password(form.password.data)
            db_sess = create_session()
            db_sess.add(user)
            db_sess.commit()
            login_user(user)
            return redirect('/')
        return render_template('register.html', message='Что-то не так', form=form)
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    global_init('db/blogs.db')
    if __name__ == '__main__':
        port = int(os.environ.get("PORT", 80))
        app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    main()
