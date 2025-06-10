# 锐视测控平台部署指南

## 🚀 快速启动

### 方法一：自动安装脚本（推荐）

#### Windows 批处理脚本
```bash
# 双击运行或在命令行中执行
setup_and_run.bat
```

#### PowerShell 脚本
```powershell
# 以管理员身份运行PowerShell，然后执行
.\setup_and_run.ps1
```

### 方法二：手动安装

#### 1. 安装Python 3.11
- 访问 https://www.python.org/downloads/
- 下载Python 3.11.x版本
- 安装时勾选"Add Python to PATH"

#### 2. 验证Python安装
```bash
python --version
pip --version
```

#### 3. 安装项目依赖
```bash
# 升级pip
python -m pip install --upgrade pip

# 安装基础依赖
pip install -r requirements.txt

# 安装额外依赖
pip install PyPDF2 python-docx
```

#### 4. 配置应用
```bash
# 复制配置文件
copy src\config.json.example src\config.json
```

#### 5. 启动应用
```bash
cd src
python main.py
```

## 🔧 配置说明

### AI API配置
编辑 `src/config.json` 文件，添加您的AI API密钥：

```json
{
  "claude": {
    "api_key": "your-claude-api-key-here",
    "default_model": "claude-3-sonnet-20240229"
  },
  "gemini": {
    "api_key": "your-gemini-api-key-here",
    "default_model": "gemini-1.5-flash"
  },
  "volcesDeepseek": {
    "api_key": "your-volces-deepseek-api-key-here",
    "url": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    "model": "deepseek-r1-250528",
    "max_tokens": 16191
  },
  "qwen-plus": {
    "api_key": "your-qwen-plus-api-key-here",
    "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    "model": "qwen-plus-2025-04-28",
    "max_tokens": 16191
  },
  "default_provider": "claude"
}
```

**注意**: 即使没有API密钥，应用也可以在演示模式下运行。

### 端口配置
默认端口：8083
访问地址：http://localhost:8083

如需修改端口，编辑 `src/main.py` 文件中的端口设置：
```python
port = int(os.getenv('PORT', 8083))  # 修改这里的端口号
```

## 🌐 访问应用

启动成功后，在浏览器中访问：
- 主页：http://localhost:8083
- 锐视测控平台：http://localhost:8083/ruishi-platform.html
- AI问答页面：http://localhost:8083/answer.html
- API健康检查：http://localhost:8083/api/health

## 📁 项目结构

```
ruishi-portal/
├── src/                          # 源代码
│   ├── config/                   # 配置模块
│   ├── models/                   # 数据模型
│   ├── routes/                   # API路由
│   ├── static/                   # 静态文件
│   ├── uploads/                  # 上传文件
│   ├── main.py                   # 应用入口
│   └── config.json              # 系统配置
├── requirements.txt              # Python依赖
├── setup_and_run.bat            # Windows批处理启动脚本
├── setup_and_run.ps1            # PowerShell启动脚本
└── DEPLOYMENT_GUIDE.md          # 本部署指南
```

## 🔍 故障排除

### 常见问题

#### 1. Python未找到
**错误**: `'python' is not recognized as an internal or external command`
**解决**: 
- 重新安装Python并勾选"Add Python to PATH"
- 或手动添加Python到系统PATH环境变量

#### 2. pip安装失败
**错误**: `pip install` 命令失败
**解决**:
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 3. 端口被占用
**错误**: `Address already in use`
**解决**:
- 修改端口号或关闭占用端口的程序
- 查看端口占用：`netstat -ano | findstr :8083`

#### 4. 模块导入错误
**错误**: `ModuleNotFoundError`
**解决**:
```bash
# 确保在正确目录
cd src

# 检查Python路径
python -c "import sys; print(sys.path)"

# 重新安装依赖
pip install -r ../requirements.txt
```

### 日志查看
应用启动时会在控制台显示详细日志，包括：
- 配置加载状态
- AI提供商初始化状态
- 服务器启动信息

### 性能优化
1. **生产环境部署**：使用Gunicorn或uWSGI
2. **静态文件**：配置Nginx代理静态文件
3. **数据库**：配置MySQL或PostgreSQL替代文件存储
4. **缓存**：添加Redis缓存层

## 🔒 安全配置

### 生产环境建议
1. 修改默认端口
2. 配置HTTPS
3. 设置防火墙规则
4. 定期更新依赖包
5. 配置日志轮转

### API密钥安全
- 不要将API密钥提交到版本控制
- 使用环境变量存储敏感信息
- 定期轮换API密钥

## 📞 技术支持

如遇到问题，请：
1. 查看控制台错误信息
2. 检查配置文件格式
3. 确认Python和依赖版本
4. 访问简仪科技官网：www.jytek.com

---

**简仪科技 JYTEK** - 专业的PXI测控解决方案提供商
