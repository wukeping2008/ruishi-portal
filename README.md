# 锐视测控平台 (SeeSharp Platform)

<div align="center">

![SeeSharp Platform](https://img.shields.io/badge/SeeSharp-Platform-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-green?style=for-the-badge&logo=python)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?style=for-the-badge&logo=javascript)
![Flask](https://img.shields.io/badge/Flask-3.1.0-red?style=for-the-badge&logo=flask)
![AI](https://img.shields.io/badge/AI-Multi--Provider-purple?style=for-the-badge)

**简仪科技专业PXI测控解决方案 | AI增强的开源测控平台**

[English](README_EN.md) | 中文

</div>

## 🌟 项目简介

锐视测控平台是由**简仪科技(JYTEK)**开发的AI增强型PXI测控门户系统，专门为模块化仪器和自动化测试领域提供智能化解决方案。平台集成了多个AI提供商，支持中英文双语，为用户提供专业的PXI技术咨询和产品推荐服务。

### 核心特性

- 🤖 **多AI集成**: 支持Claude、Gemini、Volces Deepseek、Qwen Plus四大AI提供商
- 🧠 **智能路由**: 基于问题特征自动选择最适合的AI模型
- 🌍 **国际化**: 完整的中英文双语支持
- 📚 **知识库**: 智能文档管理和AI检索系统
- 🔧 **产品配置**: 智能PXI系统方案生成器
- 📱 **响应式设计**: 支持桌面和移动设备

## 📊 项目统计

- **总代码量**: 8,833 行
- **核心文件**: 16 个
- **支持语言**: Python, JavaScript, HTML
- **AI提供商**: 4 个
- **页面数量**: 4 个

## 🏗️ 技术架构

### 后端技术栈
- **框架**: Flask 3.1.0
- **数据库**: SQLAlchemy 2.0.40
- **AI集成**: 多提供商抽象层
- **配置管理**: JSON + Python模块

### 前端技术栈
- **核心**: 原生JavaScript (ES6+)
- **样式**: Tailwind CSS
- **图标**: Font Awesome
- **国际化**: 自研i18n系统

### AI集成
- **Claude**: 复杂技术分析
- **Gemini**: 代码生成和实现
- **Volces Deepseek**: 深度推理分析
- **Qwen Plus**: 中文理解和多模态

## 🚀 快速开始

### 环境要求
- Python 3.9+
- 现代浏览器 (Chrome, Firefox, Safari, Edge)

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/jytek/ruishi-portal.git
cd ruishi-portal
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置AI API**
编辑 `src/config.json` 文件，添加您的AI API密钥：
```json
{
  "claude": {
    "api_key": "your-claude-api-key"
  },
  "gemini": {
    "api_key": "your-gemini-api-key"
  },
  "volcesDeepseek": {
    "api_key": "your-volces-api-key"
  },
  "qwen-plus": {
    "api_key": "your-qwen-api-key"
  }
}
```

4. **启动应用**
```bash
cd src
python main.py
```

5. **访问应用**
打开浏览器访问: http://localhost:5000

## 📁 项目结构

```
ruishi_portal/
├── src/                          # 源代码
│   ├── config/                   # 配置模块
│   │   └── jytek_prompts.py     # 专业提示词
│   ├── models/                   # 数据模型
│   │   ├── llm_models.py        # AI模型集成
│   │   └── knowledge.py         # 知识库模型
│   ├── routes/                   # API路由
│   │   ├── llm_routes.py        # AI问答API
│   │   ├── product_routes.py    # 产品API
│   │   └── knowledge_routes.py  # 知识库API
│   ├── static/                   # 静态资源
│   │   ├── js/                  # JavaScript文件
│   │   └── *.html               # HTML页面
│   ├── uploads/                  # 文件上传
│   ├── main.py                   # 应用入口
│   └── config.json              # 系统配置
├── requirements.txt              # Python依赖
├── README.md                     # 项目说明
└── SOFTWARE_ENGINEERING_ANALYSIS.md # 技术分析
```

## 🔧 功能模块

### 1. AI智能问答
- 支持自然语言技术咨询
- 自动选择最适合的AI模型
- 专业的PXI领域知识增强
- 中英文双语回答

### 2. 产品推荐系统
- 智能产品分类展示
- 基于需求的产品推荐
- PXI系统配置方案生成
- 详细的技术规格对比

### 3. 知识库管理
- 技术文档上传和管理
- AI驱动的文档检索
- 多格式文档支持
- 智能内容摘要

### 4. 国际化系统
- 完整的中英文界面
- 动态语言切换
- 本地化的用户体验
- 多语言内容管理

## 🌐 API接口

### AI问答接口
```http
POST /api/llm/ask
Content-Type: application/json

{
  "question": "如何选择PXI数据采集模块？",
  "provider": "claude",
  "options": {}
}
```

### 产品查询接口
```http
GET /api/products/categories
```

### 知识库接口
```http
POST /api/knowledge/upload
Content-Type: multipart/form-data

file: [文档文件]
category: "technical"
```

## 🤝 贡献指南

我们欢迎社区贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细的贡献指南。

### 开发流程
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范
- Python: 遵循 PEP 8 规范
- JavaScript: 使用 ESLint 配置
- 提交信息: 使用 Conventional Commits

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🏢 关于简仪科技

**简仪科技(JYTEK)** 是中国领先的PXI模块化测控解决方案提供商，致力于为用户提供：

- 🔬 **自主研发**: 完全自主的PXI技术和产品
- 🛡️ **自主可控**: 国产化测控解决方案
- 🎓 **技术支持**: 专业的技术培训和支持
- 🌐 **全球服务**: 面向全球的技术服务

**官网**: [www.jytek.com](https://www.jytek.com)

## 📞 联系我们

- **技术支持**: support@jytek.com
- **商务合作**: sales@jytek.com
- **官方网站**: https://www.jytek.com
- **GitHub**: https://github.com/jytek

## 🙏 致谢

感谢以下开源项目和技术提供商：

- [Flask](https://flask.palletsprojects.com/) - Web框架
- [Tailwind CSS](https://tailwindcss.com/) - CSS框架
- [Font Awesome](https://fontawesome.com/) - 图标库
- [Anthropic Claude](https://www.anthropic.com/) - AI服务
- [Google Gemini](https://deepmind.google/technologies/gemini/) - AI服务
- [Volces Deepseek](https://www.volcengine.com/) - AI服务
- [Alibaba Qwen](https://tongyi.aliyun.com/) - AI服务

## 📈 项目状态

![GitHub stars](https://img.shields.io/github/stars/jytek/ruishi-portal?style=social)
![GitHub forks](https://img.shields.io/github/forks/jytek/ruishi-portal?style=social)
![GitHub issues](https://img.shields.io/github/issues/jytek/ruishi-portal)
![GitHub license](https://img.shields.io/github/license/jytek/ruishi-portal)

---

<div align="center">

**[⬆ 回到顶部](#锐视测控平台-seesharp-platform)**

Made with ❤️ by [简仪科技 JYTEK](https://www.jytek.com)

</div>
