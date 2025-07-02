#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time

def restart_server():
    """重启服务器"""
    print("正在重启服务器...")
    
    # 杀死现有的Python进程
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                         capture_output=True, text=True)
        else:  # Unix/Linux
            subprocess.run(['pkill', '-f', 'main.py'], 
                         capture_output=True, text=True)
    except Exception as e:
        print(f"停止服务器时出错: {e}")
    
    # 等待一秒
    time.sleep(1)
    
    # 重新启动服务器
    try:
        print("启动新的服务器实例...")
        subprocess.Popen([sys.executable, 'main.py'], 
                        cwd=os.path.dirname(os.path.abspath(__file__)))
        print("服务器重启完成")
    except Exception as e:
        print(f"启动服务器时出错: {e}")

if __name__ == '__main__':
    restart_server()
