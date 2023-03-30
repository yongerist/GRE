from flask import Flask, request, jsonify
import pickle
from course import Course, BPlusNode, BPlusTree
import os

app = Flask(__name__)


# 接收post请求，执行课程增添
@app.route('/course/add', methods=['POST'])
def add():
    try:
        # 获取post请求中的数据
        id = request.form.get("id")
        name = request.form.get("name")
        begin_time = request.form.get("begin_time")
        duration = request.form.get("duration")
        week = request.form.get("week")
        offline = request.form.get("offline")

        # 建立course对象
        course = Course(id=id, name=name, begin_time=begin_time, duration=duration, week=week, offline=offline)

        #读取文件

        #首先判断文件是否为空
        if os.path.getsize('course_data.pkl') > 0:
            with open('course_data.pkl', 'rb') as f:
                data = pickle.load(f)
            data.insert(course)
        else:
            tree = BPlusTree()
            data = tree.insert(course)

        # 存入文件
        with open('course_data.pkl', 'wb') as f:
            pickle.dumps(data, f)

        # 返回成功响应
        return jsonify({"message": "Course data saved successfully."})

        # 返回失败响应
    except:
        return jsonify({"error": "An error occurred while saving course data."}), 500  # 500为http状态码，表示无法完成请求

#执行课程删减
@app.route('/course/del', method =['POST'])
def del():

if __name__ == '__main__':
    app.run()
