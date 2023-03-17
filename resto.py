from flask import Flask,  request
import pickle

app = Flask(__name__)

#接收post请求
@app.route('/save_data', methods= ['POST'])
def save_data():
    try:
        # 获取post请求中的数据
        data = request.data
        #数据反序列化为python对象
        obj = pickle.loads(data)
        #存入文件
        with open('course_data.pkl', 'wb') as f:
            pickle.dump(data, f)
    except:
        return 'error'
if __name__ == '__main__':
    app.run()
