from flask import Flask, request, jsonify, redirect, url_for, render_template, g
import pickle
from app.course import Course, BPlusNode, BPlusTree, Usr, Teacher, Student, UserManagement, MyHash
import os
from flask_login import current_user
import string

app = Flask(__name__)

course_tree_path = os.path.join(os.path.dirname(__file__), 'course_tree.pkl')
course_hash_path = os.path.join(os.path.dirname(__file__), 'course_hash.pkl')
usr_hash_path = os.path.join(os.path.dirname(__file__), 'usr_hash.pkl')


def write_tree_data(data):
    # 用于写入数据
    with open(course_tree_path, 'wb') as f:
        pickle.dump(data, f)


def write_hash_data(data):
    # 用于写入数据
    with open(course_hash_path, 'wb') as f:
        pickle.dump(data, f)


def write_usr_data(data):
    # 用于写入数据
    with open(usr_hash_path, 'wb') as f:
        pickle.dump(data, f)


a = 1
write_hash_data(a)
write_tree_data(a)
write_usr_data(a)


def load_tree_data():
    # 用于读取数据
    with open(course_tree_path, 'rb') as f:
        # 将文件中的二进制数据转换成python对象
        tree_data = pickle.load(f)
    # 返回一个B+树
    return tree_data


def load_hash_data():
    # 用于读取数据
    with open(course_hash_path, 'rb') as f:
        # 将文件中的二进制数据转换成python对象
        hash_data = pickle.load(f)
    # 返回一个哈希表
    return hash_data


def load_usr_data():
    # 用于读取数据
    with open(usr_hash_path, 'rb') as f:
        # 将文件中的二进制数据转换成python对象
        usr_data = pickle.load(f)
    # 返回一个哈希表
    return usr_data


# 接收请求前
@app.before_request
def before_request():
    # 使用g对象存储文件数据
    g.tree = load_tree_data()
    g.course_hash = load_hash_data()
    g.usr_hash = load_usr_data()
    g.manage = UserManagement(g.usr_hash)
    g.usr_id = current_user.id


# 接收post请求，展示课程列表
@app.route('/Student/course/list', methods=['GET', 'POST'])
def course_list():
    user = g.manage.login(g.usr_id)
    # 打开网页时展示课程列表
    if request.method == 'GET':
        return render_template('course_list.html', target_course=user.sort_by_name())
    # 输入待查询课程名时
    # else:
    #     name = request.form.get('name')
    #     search_type = request.form.get('search_type')
    #
    #     if os.path.getsize('course_tree.pkl') > 0:
    #         # 返回模糊查找结果列表
    #         return render_template('course_search.html', target_course=tree.prefix_search(name))
    #     else:
    #         return jsonify({"error": "An error occurred."}), 500  # 500为http状态码，表示无法完成请求


# 接收post请求，执行课程增添
@app.route('/course_list/add', methods=['GET', 'POST'])
def course_add():
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


# 执行课程删减
@app.route('/course/list/<string:id_>/del')
def course_del(id_):
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


# 执行课程修改
@app.route('/course_list/<string:course_id>/revise', methods=['GET', 'POST'])
def course_revise(course_id):
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


if __name__ == '__main__':
    app.run()
