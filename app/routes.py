from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home Page', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # print('11')
        return redirect(url_for('index'))
    form = LoginForm()
    # print('22')
    # if form.userNumber.data:
    #     print(form.userNumber.data)
    #     print(form.password.data)
    if form.validate_on_submit():
        # print('9')
        user = User.query.filter_by(userNumber=form.userNumber.data).first()
        # print(user.userNumber)
        if user is None or not user.check_password(form.password.data):
            # print('2')
            flash('学号或密码错误')
            return redirect(url_for('login'))
        # print('3')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            # print('4')
            next_page = url_for('index')
        return redirect(next_page)
    # print('5')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, userNumber=form.userNumber.data )
        user.set_password(form.password.data)
        db.session.add(user)
        # print(user.email, user.userNumber, user.username)
        db.session.commit()
        # print(user.email, user.userNumber, user.username)
        flash('恭喜, 注册成功!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)