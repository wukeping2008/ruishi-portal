import sys
import os
sys.path.insert(0, 'src')

from flask import Flask

# 创建简单的测试应用
app = Flask(__name__, static_folder='src/static', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/test')
def test():
    return "Flask应用正常运行！"

if __name__ == '__main__':
    print("启动测试服务器...")
    print("访问 http://localhost:8083 查看首页")
    print("访问 http://localhost:8083/test 查看测试页面")
    app.run(host='0.0.0.0', port=8083, debug=True)
