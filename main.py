from flask import *
import os
from data import db_session
from forms.user import RegisterForm
from flask_login import *
from data.users import User
from data.games import Games
from flask_wtf import *
from wtforms import *
from wtforms.validators import *
import future
from sqlite3 import connect
con = connect('db/blogs.db', check_same_thread=False)
cur = con.cursor()


# from console_snake import *
# import requests as request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/blogs.db")


l = 0
ButtonPressed = 1


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/game")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


#
@app.route('/game', methods=["GET", "POST"])
def button():

    global ButtonPressed
    if request.method == "POST":
        # import console_snake
        if ButtonPressed:
            os.system(r'C:\Users\Я\AppData\Local\Programs\Python\Python311\python.exe'
                      rf' C:\Users\Я\PycharmProjects\pythonProject3112\console_snake.py "{current_user.id}"')
        ButtonPressed = not ButtonPressed
        return render_template("contact.html", ButtonPressed=ButtonPressed, text=open('log.txt').read())

        # I think you want to increment, that case ButtonPressed will be plus 1.
    return render_template("contact.html", ButtonPressed=ButtonPressed, text=open('log.txt').read())


@app.route('/user', methods=['POST'])
@login_required
def user_page():
    with open('input.txt') as fi:
        l = fi.readline().strip()
    file = open('input.txt', 'w')
    if request.method == 'POST':
        if True:
            if request.data ==  b'ArrowRight':
                print('d', file=file)
                cur.execute(f'''Update games Set input='{'d'}'
                			WHERE user_id={current_user.id}''')
            elif request.data ==  b'ArrowLeft':
                print('a', file=file)
                cur.execute(f'''Update games Set input='{'a'}'
                                			WHERE user_id={current_user.id}''')
            elif request.data ==  b'ArrowDown':
                print('s', file=file)
                cur.execute(f'''Update games Set input='{'s'}'
                                			WHERE user_id={current_user.id}''')
            elif request.data ==  b'ArrowUp':
                print('w', file=file)
                cur.execute(f'''Update games Set input='{'w'}'
                                			WHERE user_id={current_user.id}''')
        print(l, file=file)
        con.commit()
    file.close()
    return 'post'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        game = Games(user=user)
        db_sess.add(user)
        db_sess.commit()
        db_sess.add(game)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
