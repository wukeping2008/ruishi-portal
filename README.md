# 🚀 锐视测控平台 | SeeSharp Platform

<div align="center">

![Platform](https://img.shields.io/badge/Platform-PXI%20Control-blue)
![AI](https://img.shields.io/badge/AI-Powered-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-red)

**🎯 基于AI技术的智能化PXI测控解决方案平台**

*专为简仪科技JYTEK打造的开源测控生态系统*

[🌟 在线演示](#-在线演示) • [📖 快速开始](#-快速开始) • [🔧 功能特性](#-核心功能) • [📚 文档](#-文档) • [🤝 贡献](#-贡献指南)

</div>

---

## 📸 平台预览

### 🎨 现代化UI设计
- **简洁有力的首页**：黑灰渐变标题，专业高级感设计
- **AI智能问答**：一键获取PXI技术支持和解决方案
- **响应式布局**：完美适配桌面、平板、移动设备

### 🤖 AI智能助手
- **多模型支持**：Claude、Gemini、Deepseek、Qwen Plus
- **智能路由**：自动选择最适合的AI模型
- **知识库集成**：基于真实技术文档的专业回答

### 📊 管理后台
- **文档管理**：支持PDF、Word、Excel等多种格式
- **数据统计**：AI使用情况和系统监控
- **用户管理**：完整的权限控制系统

---

## 🌟 在线演示

```bash
# 克隆项目
git clone https://github.com/wukeping2008/ruishi-portal.git
cd ruishi-portal

# 安装依赖
pip install -r requirements.txt

# 启动服务
cd src && python main.py

# 访问平台
open http://localhost:8083
```



---

## 🔧 核心功能

### 🧠 AI智能问答系统
```python
# 智能特征检测
characteristics = ['pxi', 'instrumentation', 'automation', 'electronics']

# 自动模型选择
provider_scores = {
    'claude': 6.5,
    'gemini': 5.6, 
    'deepseek': 3.4,
    'qwen-plus': 4.6
}
selected = max(provider_scores, key=provider_scores.get)
```

**✨ 特色功能**
- 🎯 **智能路由**：根据问题复杂度自动选择最佳AI模型
- 📚 **知识库增强**：结合企业文档生成专业回答
- 🔄 **多语言支持**：中英文无缝切换
- 📊 **实时分析**：问题特征检测和智能分类

### 📁 知识库管理系统
- **📤 文档上传**：拖拽上传，支持多种格式
- **🔍 智能搜索**：全文检索和语义匹配
- **🏷️ 分类管理**：系统架构、产品规格、软件开发、应用笔记
- **💬 文档问答**：基于特定文档的AI问答

### 🛠️ PXI产品展示
- **📦 产品目录**：完整的PXI模块化产品线
- **⚙️ 方案配置**：智能推荐最优硬件配置
- **📋 技术规格**：详细的产品参数和性能指标
- **🔗 生态集成**：SeeSharpTools SDK和开发工具链

---

## 🏗️ 技术架构

### 🎨 前端技术栈
```html
<!-- 现代化CSS设计 -->
<style>
:root {
  --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
  --radius-xl: 24px;
}
</style>
```

- **🎨 设计系统**：Apple风格的简洁美学
- **📱 响应式布局**：CSS Grid + Flexbox
- **🌈 视觉效果**：毛玻璃、渐变、阴影
- **⚡ 性能优化**：懒加载、代码分割

### ⚙️ 后端架构
```python
# Flask应用结构
app/
├── models/          # 数据模型
│   ├── llm_models.py    # AI模型管理
│   ├── knowledge.py     # 知识库模型
│   └── database.py      # 数据库操作
├── routes/          # API路由
│   ├── llm_routes.py    # AI问答API
│   ├── knowledge_routes.py  # 知识库API
│   └── admin_routes.py  # 管理后台API
└── static/          # 静态资源
```

- **🐍 Python Flask**：轻量级Web框架
- **🗄️ SQLite数据库**：文档和用户数据存储
- **🤖 多AI集成**：统一的AI提供商接口
- **📊 RESTful API**：标准化的接口设计

---

## 📚 文档

### 🚀 快速开始

#### 环境要求
- Python 3.8+
- pip 包管理器
- 现代浏览器

#### 安装步骤
```bash
# 1. 克隆项目
git clone https://github.com/wukeping2008/ruishi-portal.git
cd ruishi-portal

# 2. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置AI API密钥
cp src/config.json.example src/config.json
# 编辑config.json，添加你的API密钥

# 5. 启动服务
cd src && python main.py
```

#### 配置说明
```json
{
  "claude": {
    "api_key": "your-claude-api-key",
    "default_model": "claude-3-sonnet-20240229"
  },
  "gemini": {
    "api_key": "your-gemini-api-key", 
    "default_model": "gemini-1.5-flash"
  },
  "default_provider": "claude"
}
```

### 📖 API文档

#### AI问答接口
```bash
POST /api/llm/ask
Content-Type: application/json

{
  "question": "简仪科技的PXI产品有哪些特色？",
  "provider": "claude",  # 可选
  "options": {
    "temperature": 0.7
  }
}
```

#### 知识库接口
```bash
# 上传文档
POST /api/knowledge/upload
Content-Type: multipart/form-data

# 搜索文档
GET /api/knowledge/documents?q=PXI&limit=10

# 删除文档
DELETE /api/knowledge/delete/{doc_id}
```

---

## 🎯 使用场景

### 🏭 工业自动化
- **测试系统集成**：PXI模块化测试平台搭建
- **数据采集方案**：多通道同步采集系统设计
- **信号处理**：实时信号分析和处理

### 🎓 教育科研
- **实验平台**：高校实验室PXI教学系统
- **科研项目**：复杂测量系统快速原型
- **人才培养**：PXI技术培训和认证

### 🔬 技术支持
- **智能客服**：24/7 AI技术支持
- **文档查询**：快速找到相关技术资料
- **方案推荐**：基于需求的智能产品推荐

---

## 🌈 特色亮点

### 🤖 AI技术创新
- **🧠 智能路由算法**：根据问题特征自动选择最佳AI模型
- **📚 知识库增强**：企业文档与AI深度融合
- **🎯 精准匹配**：语义理解和上下文分析

### 🎨 用户体验设计
- **🖼️ 现代化界面**：Apple风格的简洁设计
- **📱 响应式布局**：完美适配各种设备
- **⚡ 流畅交互**：毫秒级响应和平滑动画

### 🔧 技术架构优势
- **🏗️ 模块化设计**：松耦合的组件架构
- **🔌 插件化扩展**：易于添加新的AI提供商
- **📊 数据驱动**：完整的使用统计和分析

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 🐛 报告问题
- 使用GitHub Issues报告bug
- 提供详细的复现步骤
- 包含错误日志和环境信息

### 💡 功能建议
- 在Issues中提出新功能建议
- 描述使用场景和预期效果
- 参与社区讨论

### 🔧 代码贡献
```bash
# 1. Fork项目
# 2. 创建功能分支
git checkout -b feature/amazing-feature

# 3. 提交更改
git commit -m 'Add amazing feature'

# 4. 推送分支
git push origin feature/amazing-feature

# 5. 创建Pull Request
```

### 📝 文档贡献
- 改进README和API文档
- 添加使用示例和教程
- 翻译多语言文档

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

```
MIT License

Copyright (c) 2024 简仪科技 JYTEK

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🏢 关于简仪科技

**简仪科技（JYTEK）** 是专业的PXI模块化测控解决方案提供商，致力于为客户提供高质量的测试测量产品和服务。

### 🌐 联系我们
- **官网**：[www.jytek.com](https://www.jytek.com)
- **邮箱**：info@jytek.com
- **地址**：上海浦东芳春路300号3幢
- **电话**：021-50475899

### 🎯 产品线
- **数据采集模块**：高精度多通道数据采集
- **信号发生器**：任意波形和函数发生器
- **数字I/O模块**：高速数字输入输出
- **射频测试设备**：RF/微波测试解决方案

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=wukeping2008/ruishi-portal&type=Date)](https://star-history.com/#wukeping2008/ruishi-portal&Date)

---

<div align="center">

**🌟 如果这个项目对你有帮助，请给我们一个Star！**

**💬 有问题或建议？欢迎提交Issue或Pull Request！**

**🚀 让我们一起构建更好的PXI测控生态系统！**

---

*Made with ❤️ by [简仪科技 JYTEK](https://www.jytek.com)*

</div>
