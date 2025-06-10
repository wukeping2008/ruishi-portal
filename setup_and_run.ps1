# 锐视测控平台自动安装和启动脚本
Write-Host "正在设置锐视测控平台..." -ForegroundColor Green

# 检查Python是否已安装
try {
    $pythonVersion = python --version 2>&1
    Write-Host "发现Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python未安装，正在安装..." -ForegroundColor Yellow
    
    # 使用winget安装Python
    try {
        winget install Python.Python.3.11 --silent
        Write-Host "Python安装完成，请重新启动命令行" -ForegroundColor Green
        Read-Host "按Enter键继续..."
        exit
    } catch {
        Write-Host "自动安装失败，请手动安装Python 3.11" -ForegroundColor Red
        Write-Host "下载地址: https://www.python.org/downloads/" -ForegroundColor Yellow
        Read-Host "安装完成后按Enter键继续..."
    }
}

# 检查pip
Write-Host "检查pip..." -ForegroundColor Yellow
try {
    python -m pip --version
    Write-Host "pip可用" -ForegroundColor Green
} catch {
    Write-Host "pip不可用，正在修复..." -ForegroundColor Yellow
    python -m ensurepip --upgrade
}

# 升级pip
Write-Host "升级pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# 安装项目依赖
Write-Host "安装项目依赖..." -ForegroundColor Yellow
python -m pip install -r requirements.txt
python -m pip install PyPDF2 python-docx

# 检查配置文件
if (-not (Test-Path "src\config.json")) {
    Write-Host "创建配置文件..." -ForegroundColor Yellow
    Copy-Item "src\config.json.example" "src\config.json"
}

# 启动应用
Write-Host "启动锐视测控平台..." -ForegroundColor Green
Set-Location src
python main.py

Read-Host "按Enter键退出..."
