from app import app, db
from flask import render_template, flash, redirect, url_for, request, g, jsonify
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse
from app.course import Course, BPlusTree, Usr, UserManagement, MyHash
from app.course_doc import load_tree_data, write_tree_data, load_hash_data, write_hash_data, load_usr_data, \
    write_usr_data
import os
from flask import Flask, render_template, request


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home Page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(userNumber=form.userNumber.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('学号或密码错误')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
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
        user = User(username=form.username.data, email=form.email.data, userNumber=form.userNumber.data)
        user.set_password(form.password.data)
        g.manage.user_init(username=form.username.data, email=form.email.data, userNumber=form.userNumber.data)
        write_usr_data(g.usr_hash)
        db.session.add(user)
        # print(user.email, user.userNumber, user.username)
        db.session.commit()
        # print(user.email, user.userNumber, user.username)
        flash('恭喜, 注册成功!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.before_request
def before_request():
    # 使用g对象存储文件数据
    g.tree = load_tree_data()
    g.course_hash = load_hash_data()
    g.usr_hash = load_usr_data()
    g.manage = UserManagement(g.usr_hash)


@app.route('/Student/course/list', methods=['GET', 'POST'])
def course_list():
    g.usr_id = current_user.id
    user = g.manage.login(g.usr_id)
    # 打开网页时展示课程列表
    if request.method == 'GET':
        return render_template('student_course_list.html', target_course=user.sort_by_name())


@app.route('/course_list/add', methods=['GET', 'POST'])
def course_add():
    g.usr_id = current_user.id
    if request.method == 'POST':
        try:
            # 获取post请求中的数据
            id_ = request.form.get("id")
            name = request.form.get("name")
            begin_time = request.form.get("begin_time")
            duration = request.form.get("duration")
            week = request.form.get("week")
            offline = request.form.get("offline")

            # 建立course对象
            course = Course(id=id_, name=name, begin_time=begin_time, duration=duration, week=week, offline=offline)

            # 首先判断文件是否为空
            if os.path.getsize('course_tree.pkl') > 0:
                # 将post请求中的course对象插入到B+树中
                g.tree.insert(course)
                g.course_hash.insert(course)
            # 文件为空时，建一个空树并将课程插入到该树上
            else:
                tree = BPlusTree()
                course_hash = MyHash()
                g.tree = tree.insert(course)
                g.course_hash = course_hash.insert(course)
            # 将改动后的B+树存入文件
            write_tree_data(g.tree)
            write_hash_data(g.course_hash)
            # 重定向到课程列表
            return redirect(url_for('course_list'))

            # 返回失败响应
        except:
            return jsonify({"error": "An error occurred while saving course1 data."}), 500  # 500为http状态码，表示无法完成请求
    else:
        return render_template('add.html')


@app.route('/course/list/<string:id_>/del')
def course_del(id_):
    g.usr_id = current_user.id
    # 首先判断文件是否为空
    if os.path.getsize('course_tree.pkl') > 0:
        # 删除该id对应课程
        g.tree.remove(id_)
        g.course_hash.remove(id_)

        # 将改动后的树重新存入文件
        write_tree_data(g.tree)
        write_hash_data(g.course_hash)

        # 重定向到课程列表
        return redirect(url_for('course_list'))
    else:
        return jsonify({"error": "An error occurred."}), 500


@app.route('/course_list/<string:course_id>/revise', methods=['GET', 'POST'])
def course_revise(course_id):
    g.usr_id = current_user.id
    if request.method == 'POST':
        try:
            id_ = request.form.get("id")
            name = request.form.get("name")
            begin_time = request.form.get("begin_time")
            duration = request.form.get("duration")
            week = request.form.get("week")
            offline = request.form.get("offline")

            # 创建新结点
            course_post = Course(id=id_, name=name, begin_time=begin_time, duration=duration, week=week,
                                 offline=offline)

            # 查找需要修改的结点
            course_pre = g.course_hash.find(course_id)

            # 执行修改操作
            g.tree.revise(course_pre, course_post)

            # 将改动后的数据存入文件
            write_tree_data(g.tree)
            write_hash_data(g.course_hash)

            # 返回课程列表
            return redirect(url_for('course_list'))
        except:
            return jsonify({"error": "An error occurred."}), 500
    else:
        return render_template('revise.html')
