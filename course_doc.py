from flask import Flask, request, jsonify, redirect, url_for, render_template
import pickle
from course import Course, BPlusNode, BPlusTree
import os

app = Flask(__name__)


# 接收post请求，展示课程列表
@app.route('/course_list', methods=['POST'])
def course_list():
    # 首先判断文件是否为空
    if os.path.getsize('course_data.pkl') > 0:
        with open('course_data.pkl', 'rb') as f:
            # 将文件中的二进制数据转换成python对象
            tree = pickle.load(f)
        # 返回B+树叶子节点的信息
        return tree.get_all_data

    # 文件为空时，返回失败响应
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
            if os.path.getsize('course_data.pkl') > 0:
                with open('course_data.pkl', 'rb') as f:
                    data = pickle.load(f)

                # 将post请求中的course对象插入到B+树中
                data.insert(course)

            # 文件为空时，建一个空树并将课程插入到该树上
            else:
                tree = BPlusTree()
                data = tree.insert(course)

            # 将改动后的B+树存入文件
            with open('course_data.pkl', 'wb') as f:
                # 将data转化为二进制数据传入文件
                pickle.dump(data, f)

            # 重定向到课程列表
            return redirect(url_for(course_list))

            # 返回失败响应
        except:
            return jsonify({"error": "An error occurred while saving course data."}), 500  # 500为http状态码，表示无法完成请求
    else:
        return render_template('add.html')


# 执行课程删减
@app.route('/course_list/<string: id_>/del')
def course_del(id_):
    # 首先判断文件是否为空
    if os.path.getsize('course_data.pkl') > 0:
        with open('course_data.pkl', 'rb') as f:
            data = pickle.load(f)

        # 删除该id对应课程
        data.remove(id_)

        # 将改动后的树重新存入文件
        with open('course_data.pkl', 'wb') as f:
            pickle.dump(data, f)

        # 重定向到课程列表
        return redirect(url_for(course_list))
    else:
        return jsonify({"error": "An error occurred."}), 500


# 执行课程修改
@app.route('/course_list/<string: course_id>/revise', method=['GET', 'POST'])
def course_revise():
    if method == 'POST':
        try:
            id_ = request.form.get("id")
            name = request.form.get("name")
            begin_time = request.form.get("begin_time")
            duration = request.form.get("duration")
            week = request.form.get("week")
            offline = request.form.get("offline")

            # 创建新结点
            course_post = Course(id=id_, name=name, begin_time=begin_time, duration=duration, week=week,offline=offline)

            # 打开文件加载数据
            with open('course_data.pkl', 'rb') as f:
                data = pickle.load(f)

            # 查找需要修改的结点
            course_pre = data.find(key=course_id)

            # 执行修改操作
            data.revise(course_pre, course_post)

            # 将改动后的数据存入文件
            with open('course_data.pkl', 'wb') as f:
                pickle.dump(data, f)

            # 返回课程列表
            return redirect(url_for(course_list))
        except:
            return jsonify({"error": "An error occurred."}), 500
    else:
        return render_template('revise.html')


if __name__ == '__main__':
    app.run()
