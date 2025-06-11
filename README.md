# 简仪科技锐视测控平台

## 项目简介

简仪科技锐视测控平台是一个基于AI技术的智能测控解决方案平台，为客户提供专业的PXI/PXIe测试测量产品和技术支持服务。

## 主要功能

### 🤖 AI智能助手
- 基于大语言模型的智能问答系统
- 支持多种AI模型（Claude、Gemini、通义千问、DeepSeek等）
- 智能模型选择和负载均衡
- 专业的测控领域知识库支持

### 📚 知识库管理
- 技术文档智能检索
- 向量化文档存储
- 多格式文档支持（PDF、DOCX、XLSX等）
- 智能内容推荐

### 🛠️ 产品中心
- **PXIe控制器** - 高性能嵌入式控制器
- **数据采集卡** - 高精度、高速率数据采集解决方案
- **任意波形发生器** - 灵活的信号生成解决方案
- **数字化仪** - 高速数字化仪，提供出色的信号捕获和分析能力
- **PXIe机箱** - 高性能PXIe机箱，提供稳定的电源和信号传输
- **数字I/O模块** - 灵活的数字输入输出解决方案

### 📊 管理后台
- 用户对话统计分析
- 关键词使用统计
- 文档使用情况分析
- 系统性能监控

## 技术架构

### 后端技术栈
- **Python Flask** - Web框架
- **SQLAlchemy** - ORM数据库操作
- **ChromaDB** - 向量数据库
- **Sentence Transformers** - 文本向量化
- **OpenAI API** - AI模型接口
- **SQLite** - 数据存储

### 前端技术栈
- **HTML5/CSS3/JavaScript** - 基础前端技术
- **Tailwind CSS** - 样式框架
- **Font Awesome** - 图标库
- **响应式设计** - 适配多种设备

### AI模型支持
- **Claude** (Anthropic)
- **Gemini** (Google)
- **通义千问** (阿里云)
- **DeepSeek** (深度求索)

## 项目结构

```
ruishi-portal/
├── src/
│   ├── main.py                 # 主应用入口
│   ├── models/                 # 数据模型
│   │   ├── ai_conversation.py  # AI对话记录
│   │   ├── enhanced_knowledge.py # 知识库管理
│   │   ├── llm_models.py       # LLM模型管理
│   │   └── products.py         # 产品数据模型
│   ├── static/                 # 静态文件
│   │   ├── index.html          # 主页
│   │   ├── products.html       # 产品中心
│   │   ├── knowledge.html      # 知识库
│   │   ├── admin.html          # 管理后台
│   │   └── js/                 # JavaScript文件
│   ├── uploads/                # 上传文件目录
│   └── database/               # 数据库文件
├── requirements.txt            # Python依赖
└── README.md                   # 项目说明
```

## 安装和运行

### 环境要求
- Python 3.8+
- pip包管理器

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/your-username/ruishi-portal.git
cd ruishi-portal
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
创建 `.env` 文件并配置API密钥：
```
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key
QWEN_API_KEY=your_qwen_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
```

4. 运行应用
```bash
cd src
python main.py
```

5. 访问应用
打开浏览器访问 `http://localhost:5000`

## 主要特性

### 🎯 智能模型选择
系统会根据问题特征自动选择最适合的AI模型：
- **代码相关问题** → Claude
- **数学计算问题** → Claude/Gemini
- **通用问题** → 通义千问
- **简单问题** → DeepSeek

### 📈 负载均衡
- 智能分发请求到不同模型
- 避免单一模型过载
- 提高系统整体性能

### 🔍 智能检索
- 基于向量相似度的文档检索
- 支持中英文混合检索
- 智能内容摘要和推荐

### 📱 响应式设计
- 适配桌面、平板、手机等设备
- 现代化UI设计
- 流畅的用户体验

## 应用领域

- **工业自动化** - 生产线测试、质量控制、设备监控
- **汽车电子** - ECU测试、HIL仿真、电池管理系统测试
- **航空航天** - 航电设备测试、雷达系统测试、卫星通信测试
- **教育科研** - 实验室建设、科研项目、教学实验
- **通信电子** - 5G设备测试、基站测试、射频器件测试
- **医疗设备** - 医疗器械测试、生物信号采集、设备校准

## 联系我们

- **公司**: 上海简仪科技有限公司
- **电话**: 400-123-4567
- **邮箱**: info@jytek.com
- **网站**: www.jytek.com
- **地址**: 上海市浦东新区

## 许可证

Copyright © 2024 简仪科技. 保留所有权利.
