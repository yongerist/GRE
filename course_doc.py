from flask import Flask, request, jsonify
import pickle
from course import Course

app = Flask(__name__)


# 接收post请求
@app.route('/course', methods=['POST'])
def save_data():
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
        # 存入文件
        with open('course_data.pkl', 'wb') as f:
            pickle.dumps(course, f)
        # 返回成功响应
        return jsonify({"message": "Course data saved successfully."})
    except:
        # 返回失败响应
        return jsonify({"error": "An error occurred while saving course data."}), 500  # 500为http状态码，表示无法完成请求


if __name__ == '__main__':
    app.run()
