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
    if (form.userNumber.data == '0') and (form.password.data == '0'):
        return redirect(url_for('teacher_index'))
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


@app.route('/teacher/index')
def teacher_index():
    return render_template("teacher_index.html")


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
        print(g.manage.user_table.my_hash_table)
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
    g.usr_id = current_user.userNumber
    print(g.usr_id)
    user = g.manage.login(g.usr_id)
    # print(user.course[0].name)
    # for obj in user.sort_by_name():
    #    print(obj.name)
    # 打开网页时展示课程列表
    if request.method == 'GET':
        return render_template('student_course_list.html', queryset=user.sort_by_name())


@app.route('/del/all', methods=['GET', 'POST'])
def del_all():
    db.session.query(User).delete()
    db.session.commit()
    return "delete success"


@app.route('/all/course/list', methods=['GET', 'POST'])
def all_course_list():
    if request.method == 'GET':
        return render_template('teacher_course_list.html', queryset=g.tree.get_all_data())


@app.route('/course_list/add', methods=['GET', 'POST'])
def course_add():
    if request.method == 'POST':
        # try:
        # 获取post请求中的数据
        # id_ = int(request.form.get("id"))
        name = request.form.get("name")
        day = request.form.getlist("day[]")
        begin_time = request.form.get("begin_time")
        end_time = request.form.get("end_time")
        week = request.form.getlist("week[]")
        offline = request.form.get("method")
        student = request.form.getlist("student[]")

        # student = [1]
        # 建立course对象
        course = Course(name=name, day=day, begin_time=begin_time, end_time=end_time, week=week, offline=offline,
                        student=student)

        if g.manage.time_conflicts(course):
            # 将post请求中的course对象插入到B+树中
            g.tree.insert(course)
            g.course_hash.insert(course)
            print(course.student)
            for st in course.student:
                g.manage.user_table.find(st).course.append(course)
                print(g.manage.user_table.find(st))
            # 将改动后的B+树存入文件
            write_tree_data(g.tree)
            write_hash_data(g.course_hash)
            # 将改动后的B+树存入文件
            write_tree_data(g.tree)
            write_hash_data(g.course_hash)
            write_usr_data(g.usr_hash)
        # 重定向到课程列表
        return redirect(url_for('all_course_list'))

        # 返回失败响应
        # except:
        #     return jsonify({"error": "An error occurred while saving course1 data."}), 500  # 500为http状态码，表示无法完成请求
    else:
        return render_template('teacher_course_add.html', student=g.manage.all_student())


@app.route('/course/<int:id_>/del/', methods=['GET', 'POST'])
def course_del(id_):
    # 首先判断文件是否为空
    # if os.path.getsize(course_tree_path) > 0:
    # 删除该id对应课程
    course = g.course_hash.find(id_)
    print(id_)
    name = course.name
    student = course.student
    print(name)
    g.tree.remove(g.course_hash.find(id_).name)
    g.course_hash.remove(id_)
    for st in student:
        g.manage.user_table.find(st).course.remove(course)
    # 将改动后的树重新存入文件
    write_tree_data(g.tree)
    write_hash_data(g.course_hash)
    write_usr_data(g.usr_hash)
    # 重定向到课程列表
    return redirect(url_for('all_course_list'))
    # else:
    #     return jsonify({"error": "An error occurred."}), 500


@app.route('/course_list/<string:course_id>/revise', methods=['GET', 'POST'])
def course_revise(course_id):
    g.usr_id = current_user.id
    if request.method == 'POST':
        try:
            # try:
            # 获取post请求中的数据
            id_ = request.form.get("id")
            name = request.form.get("name")
            day = request.form.getlist("day[]")
            begin_time = request.form.get("begin_time")
            end_time = request.form.get("end_time")
            week = request.form.getlist("week[]")
            offline = request.form.get("method")
            # 建立course对象
            course_post = Course(id=id_, name=name, day=day, begin_time=begin_time, end_time=end_time, week=week,
                                 offline=offline)

            # 查找需要修改的结点
            course_pre = g.course_hash.find(course_id)

            # 执行修改操作
            g.tree.revise(course_pre, course_post)

            # 将改动后的数据存入文件
            write_tree_data(g.tree)
            write_hash_data(g.course_hash)

            # 返回课程列表
            return redirect(url_for('all_course_list'))
        except:
            return jsonify({"error": "An error occurred."}), 500
    else:
        return render_template('teacher_course_edit.html')
