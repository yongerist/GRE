from flask import flash, redirect, url_for, g
from flask import render_template, request
from flask_login import current_user, login_user
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.course import Course, UserManagement, Activity
from app.course_doc import load_tree_data, write_tree_data, load_hash_data, write_hash_data, load_usr_data, \
    write_usr_data, load_gro_act_tree_data, write_gro_act_tree_data
from app.forms import LoginForm, RegistrationForm
from app.models import User


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
    g.gro_act_tree = load_gro_act_tree_data()
    g.course_hash = load_hash_data()
    g.usr_hash = load_usr_data()
    g.manage = UserManagement(g.usr_hash)


@app.route('/Student/course/list', methods=['GET', 'POST'])
def course_list():
    g.usr_id = current_user.id - 1
    print(g.usr_id)
    user = g.manage.login(g.usr_id)

    # 打开网页时展示课程列表
    if request.method == 'GET':
        return render_template('student_course_list.html', queryset=user.sort_by_name(g.course_hash))


@app.route('/del/all', methods=['GET', 'POST'])
def del_all():
    db.session.query(User).delete()
    db.session.commit()
    return "delete success"


@app.route('/all/course/list', methods=['GET', 'POST'])
def all_course_list():
    if request.method == 'GET':
        return render_template('teacher_course_list.html', queryset=g.tree.get_all_data())


@app.route('/course/<int:id_>/info/', methods=['GET', 'POST'])
def course_info(id_):
    course = g.course_hash.find(id_)
    print('id=' + str(id_))
    name = course.name
    print(name)
    time = []
    for week in course.week:
        for day in course.day:
            time.append(f'第{week}周   周{day}   {course.begin_time[0]}时{course.begin_time[1]}分--{course.end_time[0]}时{course.end_time[1]}分')
    students = []
    for obj in course.student:
        print(obj)
        obj = int(obj)
        print(type(obj))
        user = User.query.filter_by(id=obj+1).first()
        print(user)
        students.append(str(user.username))
    return render_template('teacher_course_info.html', course=course, time=time, students=students)


@app.route('/group_activity/<string:name>/info/', methods=['GET', 'POST'])
def group_activity_info(name):
    print(name)
    print(type(name))
    activity = g.gro_act_tree.find(name)
    time = []
    for week in activity.week:
        for day in activity.day:
            time.append(f'第{week}周   周{day}   {activity.begin_time[0]}时{activity.begin_time[1]}分--{activity.end_time[0]}时')
    students = []
    for obj in activity.student:
        obj = int(obj)
        user = User.query.filter_by(id=obj+1).first()
        students.append(str(user.username))
    return render_template('teacher_group_activity_info.html', activity=activity, time=time, students=students)


@app.route('/group_activity/list', methods=['GET', 'POST'])
def group_activity_list():
    if request.method == 'GET':
        return render_template('teacher_group_activity_list.html', queryset=g.gro_act_tree.get_all_data())


@app.route('/course_list/add', methods=['GET', 'POST'])
def course_add():
    error = None
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
        for obj in student:
            print(obj)
        # student = [1]
        # 建立course对象
        course = Course(name=name, day=day, begin_time=begin_time, end_time=end_time, week=week, offline=offline,
                        student=student)
        if g.manage.time_conflicts(course):
            # 将post请求中的course对象插入到B+树中
            g.tree.insert(course)
            g.course_hash.insert(course)
            g.manage.add_student_course(course)
            # 将改动后的B+树存入文件
            write_tree_data(g.tree)
            write_hash_data(g.course_hash)
            write_usr_data(g.usr_hash)
            # 重定向到课程列表
            print('添加成功')
            flash('添加成功!')
            return redirect(url_for('all_course_list'))
        else:
            print('添加失败')
            error = "时间已经被占用,添加失败!"
            return render_template('teacher_course_add.html', student=g.manage.all_student(), error=error)
        # 返回失败响应
        # except:
        #     return jsonify({"error": "An error occurred while saving course1 data."}), 500  # 500为http状态码，表示无法完成请求
    else:
        return render_template('teacher_course_add.html', student=g.manage.all_student(), error=error)


@app.route('/group_activity/add', methods=['GET', 'POST'])
def group_activity_add():
    error = None
    if request.method == 'POST':
        # try:
        # 获取post请求中的数据
        # id_ = int(request.form.get("id"))
        name = request.form.get("name")
        day = request.form.getlist("day[]")
        begin_time = request.form.get("begin_time")
        week = request.form.getlist("week[]")
        offline = request.form.get("method")
        student = request.form.getlist("student[]")
        for obj in student:
            print(obj)
        # student = [1]
        # 建立course对象
        activity = Activity(name=name, day=day, begin_time=begin_time, week=week, offline=offline,
                            student=student)
        if g.manage.time_conflicts(activity):
            # 将post请求中的course对象插入到B+树中
            g.gro_act_tree.insert(activity)
            g.manage.add_student_activities(activity)
            # 将改动后的B+树存入文件
            write_gro_act_tree_data(g.gro_act_tree)
            write_usr_data(g.usr_hash)
            # 重定向到课程列表
            print('添加成功')
            flash('添加成功!')
            return redirect(url_for('group_activity_list'))
        else:
            print('添加失败')
            error = "时间已经被占用,添加失败!"
            return render_template('teacher_group_activity_add.html', student=g.manage.all_student(), error=error)
    else:
        return render_template('teacher_group_activity_add.html', student=g.manage.all_student(), error=error)


@app.route('/group_activity/<string:name>/del/', methods=['GET', 'POST'])
def group_activity_del(name):
    activity = g.gro_act_tree.find(name)
    student = activity.student
    g.gro_act_tree.remove(name)
    for st in student:
        g.manage.del_student_activities(activity)
    # 将改动后的树重新存入文件
    write_gro_act_tree_data(g.gro_act_tree)
    write_usr_data(g.usr_hash)
    # 重定向到课程列表
    return redirect('/group_activity/list')


# 修改课程
@app.route('/course/<int:course_id>/edit/', methods=['GET', 'POST'])
def course_revise(course_id):
    course_old = g.course_hash.find(course_id)
    print(course_old.name)
    error = None
    if request.method == 'POST':
        name = request.form.get("name")
        day = request.form.getlist("day[]")
        begin_time = request.form.get("begin_time")
        end_time = request.form.get("end_time")
        week = request.form.getlist("week[]")
        offline = request.form.get("method")
        student = request.form.getlist("student[]")
        # 建立course对象
        course = Course(name=name, day=day, begin_time=begin_time, end_time=end_time, week=week, offline=offline,
                        student=student)
        if g.manage.revise_time_conflicts(course_old, course):
            # 将post请求中的course对象插入到B+树中
            g.tree.revise(course_old, course)
            g.course_hash.revise(course_old, course)
            g.manage.revise_student_course(course_old, course)
            # 将改动后的B+树存入文件
            write_tree_data(g.tree)
            write_hash_data(g.course_hash)
            # 将改动后的B+树存入文件
            write_tree_data(g.tree)
            write_hash_data(g.course_hash)
            write_usr_data(g.usr_hash)
            # 重定向到课程列表
            print('修改成功')
            flash('修改成功!')
            return redirect(url_for('all_course_list'))
        else:
            print('修改失败')
            error = "时间已经被占用,添加失败!"
            return render_template('teacher_course_add.html', student=g.manage.all_student(), error=error)
        # 返回失败响应
        # except:
        #     return jsonify({"error": "An error occurred while saving course1 data."}), 500  # 500为http状态码，表示无法完成请求
    else:
        return render_template('teacher_course_edit.html', course=course_old, student=g.manage.all_student())
