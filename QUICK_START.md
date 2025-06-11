# 🚀 锐视测控平台 - 快速部署指南

## 📋 系统要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **内存**: 最少 2GB RAM
- **存储**: 最少 1GB 可用空间
- **网络**: 需要访问AI API服务

## ⚡ 一键启动

### Windows 用户
```bash
# 双击运行
setup_and_run.bat
```

### macOS/Linux 用户
```bash
# 终端运行
chmod +x setup_and_run.sh
./setup_and_run.sh
```

### 手动安装
```bash
# 1. 克隆项目
git clone https://github.com/wukeping2008/ruishi-portal.git
cd ruishi-portal

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
cd src && python main.py

# 4. 访问平台
open http://localhost:8083
```

## 🔧 配置AI服务

### 1. 复制配置文件
```bash
cp src/config.json.example src/config.json
```

### 2. 编辑配置文件
```json
{
  "claude": {
    "api_key": "sk-ant-api03-your-claude-key",
    "default_model": "claude-3-sonnet-20240229"
  },
  "gemini": {
    "api_key": "your-gemini-api-key",
    "default_model": "gemini-1.5-flash"
  },
  "volcesDeepseek": {
    "api_key": "your-deepseek-key",
    "default_model": "deepseek-chat"
  },
  "qwen-plus": {
    "api_key": "your-qwen-key", 
    "default_model": "qwen-plus"
  },
  "default_provider": "claude"
}
```

### 3. 获取API密钥

#### Claude API
1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 创建账户并获取API密钥
3. 将密钥填入 `claude.api_key`

#### Gemini API
1. 访问 [Google AI Studio](https://makersuite.google.com/)
2. 创建项目并获取API密钥
3. 将密钥填入 `gemini.api_key`

#### Deepseek API
1. 访问 [Deepseek Platform](https://platform.deepseek.com/)
2. 注册并获取API密钥
3. 将密钥填入 `volcesDeepseek.api_key`

#### Qwen API
1. 访问 [阿里云百炼](https://bailian.console.aliyun.com/)
2. 开通服务并获取API密钥
3. 将密钥填入 `qwen-plus.api_key`

## 🎮 功能测试

### 1. AI问答测试
- 访问首页：http://localhost:8083
- 在搜索框输入：`简仪科技的PXI产品有哪些特色？`
- 点击"提问"按钮
- 查看AI回答

### 2. 知识库测试
- 访问知识库：http://localhost:8083/knowledge.html
- 上传测试文档（PDF、Word、Excel）
- 搜索文档内容
- 测试文档问答功能

### 3. 管理后台测试
- 访问管理后台：http://localhost:8083/admin/dashboard
- 使用账号：`admin` / `admin123`
- 查看系统统计
- 管理文档和用户

## 🔍 故障排除

### 常见问题

#### 1. 端口被占用
```bash
# 查看端口占用
lsof -i :8083  # macOS/Linux
netstat -ano | findstr :8083  # Windows

# 修改端口
export PORT=8084  # 设置环境变量
cd src && python main.py
```

#### 2. Python版本问题
```bash
# 检查Python版本
python --version

# 使用Python 3
python3 main.py
```

#### 3. 依赖安装失败
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 4. AI API调用失败
- 检查API密钥是否正确
- 确认网络连接正常
- 查看控制台错误日志
- 尝试切换AI提供商

### 日志查看
```bash
# 查看详细日志
cd src && python main.py --debug

# 查看错误日志
tail -f logs/error.log  # 如果有日志文件
```

## 🌐 生产部署

### Docker部署
```bash
# 构建镜像
docker build -t ruishi-portal .

# 运行容器
docker run -p 8083:8083 -v $(pwd)/src/data:/app/src/data ruishi-portal
```

### Nginx反向代理
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8083;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 环境变量配置
```bash
# 设置环境变量
export CLAUDE_API_KEY="your-claude-key"
export GEMINI_API_KEY="your-gemini-key"
export PORT=8083
export FLASK_ENV=production
```

## 📞 技术支持

### 获取帮助
- **GitHub Issues**: [提交问题](https://github.com/wukeping2008/ruishi-portal/issues)
- **官方网站**: [www.jytek.com](https://www.jytek.com)
- **技术文档**: [查看Wiki](https://github.com/wukeping2008/ruishi-portal/wiki)

### 社区交流
- **QQ群**: 123456789 (锐视测控技术交流)
- **微信群**: 扫描二维码加入
- **邮箱支持**: support@jytek.com

---

**🎯 快速开始，立即体验AI驱动的PXI测控平台！**
