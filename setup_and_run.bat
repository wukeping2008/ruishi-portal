@echo off
echo 正在设置锐视测控平台...

REM 检查Python是否已安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python未安装，正在安装Python...
    
    REM 使用winget安装Python
    winget install Python.Python.3.11 --silent
    
    REM 刷新环境变量
    call refreshenv
    
    REM 等待安装完成
    timeout /t 10 /nobreak
)

REM 再次检查Python
python --version
if %errorlevel% neq 0 (
    echo Python安装失败，请手动安装Python 3.11
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python已安装，版本信息:
python --version

echo 正在安装项目依赖...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install PyPDF2 python-docx

echo 检查配置文件...
if not exist "src\config.json" (
    echo 创建配置文件...
    copy "src\config.json.example" "src\config.json"
)

echo 启动锐视测控平台...
cd src
python main.py

pause
