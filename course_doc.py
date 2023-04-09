from flask import Flask, request, jsonify, redirect, url_for, render_template, g
import pickle
from course import Course, BPlusNode, BPlusTree, User, Teacher, Student, UserManagement
import os
import string

app = Flask(__name__)


def load_tree_data():
    # 用于读取数据
    with open('course_tree.pkl', 'rb') as f:
        # 将文件中的二进制数据转换成python对象
        tree_data = pickle.load(f)
    # 返回一个B+树
    return tree_data


def write_tree_data(data):
    # 用于写入数据
    with open('course_tree.pkl', 'wb') as f:
        pickle.dump(data, f)


def load_hash_data():
    # 用于读取数据
    with open('course_hash.pkl', 'rb') as f:
        # 将文件中的二进制数据转换成python对象
        hash_data = pickle.load(f)
    # 返回一个哈希表
    return hash_data


def write_hash_data(data):
    # 用于写入数据
    with open('course_hash.pkl', 'wb') as f:
        pickle.dump(data, f)


def load_usr_data():
    # 用于读取数据
    with open('usr_hash.pkl', 'rb') as f:
        # 将文件中的二进制数据转换成python对象
        usr_data = pickle.load(f)
    # 返回一个哈希表
    return usr_data


def write_usr_data(data):
    # 用于写入数据
    with open('usr_hash.pkl', 'wb') as f:
        pickle.dump(data, f)


# 接收请求前
@app.before_request
def before_request():
    # 使用g对象存储文件数据
    g.tree = load_tree_data()
    g.course_hash = load_hash_data()
    g.usr_hash = load_usr_data()
    management = UserManagement(g.user_hash)
    g.usr = management.login()


# 接收post请求，展示课程列表
@app.route('/User/course/list', methods=['GET', 'POST'])
def course_list():
    # 打开网页时展示课程列表
    if request.method == 'GET':
        # 首先判断文件是否为空
        if os.path.getsize('course_tree.pkl') > 0:
            # 返回B+树叶子节点的信息
            return render_template('course_list.html', target_course=g.data.get_all_data)
        # 文件为空时，返回失败响应
        else:
            return jsonify({"error": "An error occurred."}), 500  # 500为http状态码，表示无法完成请求
    # 输入待查询课程名时
    else:
        name = request.form.get('name')
        type_search = request.form.get('type_search')
        if os.path.getsize('course_tree.pkl') > 0:
            # 返回模糊查找结果列表
            return render_template('course_search.html', target_course=tree.prefix_search(name))
        else:
            return jsonify({"error": "An error occurred."}), 500  # 500为http状态码，表示无法完成请求


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

            # 读取文件

            # 首先判断文件是否为空
            if os.path.getsize('course_tree.pkl') > 0:
                with open('course_tree.pkl', 'rb') as f:
                    data = pickle.load(f)

                # 将post请求中的course对象插入到B+树中
                data.insert(course)

            # 文件为空时，建一个空树并将课程插入到该树上
            else:
                tree = BPlusTree()
                data = tree.insert(course)

            # 将改动后的B+树存入文件
            with open('course_tree.pkl', 'wb') as f:
                # 将data转化为二进制数据传入文件
                pickle.dump(data, f)

            # 重定向到课程列表
            return redirect(url_for('course_list'))

            # 返回失败响应
        except:
            return jsonify({"error": "An error occurred while saving course data."}), 500  # 500为http状态码，表示无法完成请求
    else:
        return render_template('add.html')


# 执行课程删减
@app.route('/course_list/<string:id_>/del')
def course_del(id_):
    # 首先判断文件是否为空
    if os.path.getsize('course_tree.pkl') > 0:
        with open('course_tree.pkl', 'rb') as f:
            data = pickle.load(f)

        # 删除该id对应课程
        data.remove(id_)

        # 将改动后的树重新存入文件
        with open('course_tree.pkl', 'wb') as f:
            pickle.dump(data, f)

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

            # 打开文件加载数据
            with open('course_tree.pkl', 'rb') as f:
                data = pickle.load(f)

            # 查找需要修改的结点
            course_pre = data.find(key=course_id)

            # 执行修改操作
            data.revise(course_pre, course_post)

            # 将改动后的数据存入文件
            with open('course_tree.pkl', 'wb') as f:
                pickle.dump(data, f)

            # 返回课程列表
            return redirect(url_for('course_list'))
        except:
            return jsonify({"error": "An error occurred."}), 500
    else:
        return render_template('revise.html')


if __name__ == '__main__':
    app.run()
