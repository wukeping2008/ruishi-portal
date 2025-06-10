"""
调试服务器 - 用于诊断Flask应用问题
"""

import os
import sys
from flask import Flask, send_from_directory

# 获取当前脚本目录
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'src', 'static')

print(f"当前目录: {current_dir}")
print(f"静态文件目录: {static_dir}")
print(f"静态文件目录存在: {os.path.exists(static_dir)}")

if os.path.exists(static_dir):
    files = os.listdir(static_dir)
    print(f"静态文件列表: {files}")
    
    index_path = os.path.join(static_dir, 'index.html')
    print(f"index.html存在: {os.path.exists(index_path)}")
    
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"index.html文件大小: {len(content)} 字符")
            print(f"文件开头: {content[:100]}...")

# 创建Flask应用
app = Flask(__name__, static_folder=static_dir, static_url_path='')

@app.route('/')
def index():
    """主页路由"""
    try:
        print("访问主页路由")
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        print(f"错误: {e}")
        return f"<h1>错误</h1><p>{e}</p><p>静态文件夹: {app.static_folder}</p>"

@app.route('/debug')
def debug():
    """调试信息"""
    return f"""
    <h1>调试信息</h1>
    <p>静态文件夹: {app.static_folder}</p>
    <p>静态文件夹存在: {os.path.exists(app.static_folder)}</p>
    <p>index.html存在: {os.path.exists(os.path.join(app.static_folder, 'index.html'))}</p>
    <p>当前工作目录: {os.getcwd()}</p>
    """

@app.route('/test')
def test():
    """测试路由"""
    return "<h1>测试成功！Flask应用正常运行</h1>"

if __name__ == '__main__':
    print("=" * 50)
    print("启动调试服务器")
    print("=" * 50)
    print(f"访问 http://localhost:8083 查看主页")
    print(f"访问 http://localhost:8083/debug 查看调试信息")
    print(f"访问 http://localhost:8083/test 查看测试页面")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=8083, debug=True)
