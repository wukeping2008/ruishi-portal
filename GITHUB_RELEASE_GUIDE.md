# 📚 GitHub发布指南 | GitHub Release Guide

本指南将帮助您将锐视测控平台项目发布到GitHub。

## 🚀 快速发布步骤

### 1. 创建GitHub仓库

1. 登录 [GitHub](https://github.com)
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `ruishi-portal`
   - **Description**: `🚀 锐视测控平台 - 基于AI技术的智能化PXI测控解决方案平台`
   - **Visibility**: Public (推荐) 或 Private
   - **不要**勾选 "Initialize this repository with a README"
4. 点击 "Create repository"

### 2. 连接本地仓库到GitHub

```bash
# 添加远程仓库 (替换YOUR_USERNAME为你的GitHub用户名)
git remote add origin https://github.com/YOUR_USERNAME/ruishi-portal.git

# 推送代码到GitHub
git branch -M main
git push -u origin main
```

### 3. 验证发布

访问你的GitHub仓库页面，确认：
- ✅ 所有文件已正确上传
- ✅ README.md正确显示
- ✅ 项目描述和标签正确

## 📋 发布前检查清单

### 🔒 安全检查
- [ ] 确认 `src/config.json` 已被 `.gitignore` 忽略
- [ ] 检查没有API密钥被意外提交
- [ ] 验证数据库文件不包含敏感信息
- [ ] 确认上传的文档不包含机密内容

### 📁 文件检查
- [ ] README.md 内容完整且格式正确
- [ ] LICENSE 文件存在
- [ ] requirements.txt 包含所有依赖
- [ ] .gitignore 配置完善
- [ ] 项目结构清晰

### 🧪 功能测试
- [ ] 本地服务正常启动
- [ ] AI问答功能正常
- [ ] 文档上传功能正常
- [ ] 管理后台可访问
- [ ] 所有页面响应正常

## 🏷️ 创建Release版本

### 1. 创建标签
```bash
# 创建v1.0.0标签
git tag -a v1.0.0 -m "🚀 锐视测控平台 v1.0.0 正式发布

✨ 主要功能:
- AI智能问答系统
- 知识库管理
- PXI产品展示
- 管理后台
- 提示词优化系统

🎯 适用场景:
- 工业自动化测试
- 教育科研实验
- 技术支持服务"

# 推送标签到GitHub
git push origin v1.0.0
```

### 2. 在GitHub上创建Release

1. 进入GitHub仓库页面
2. 点击右侧的 "Releases"
3. 点击 "Create a new release"
4. 选择刚创建的标签 `v1.0.0`
5. 填写Release信息：

**Release title**: `🚀 锐视测控平台 v1.0.0`

**Release notes**:
```markdown
## 🎉 锐视测控平台 v1.0.0 正式发布！

### ✨ 核心功能
- 🤖 **AI智能问答系统**: 支持Claude、Gemini、Deepseek、Qwen Plus多模型
- 📚 **知识库管理系统**: 文档上传、搜索、分类管理
- 🛠️ **PXI产品展示**: 完整的产品线和方案配置
- 📊 **管理后台**: 用户管理、数据统计、系统监控
- 🎯 **提示词优化系统**: 多模式配置管理

### 🎨 技术特色
- 现代化UI设计 (Apple风格简洁美学)
- 响应式布局 (完美适配各种设备)
- 智能路由算法 (自动选择最佳AI模型)
- 模块化架构 (Flask + SQLite + RESTful API)

### 🚀 快速开始
```bash
git clone https://github.com/YOUR_USERNAME/ruishi-portal.git
cd ruishi-portal
pip install -r requirements.txt
cd src && python main.py
```

### 📖 文档
- [快速开始指南](QUICK_START.md)
- [部署指南](DEPLOYMENT_GUIDE.md)
- [API文档](README.md#-api文档)

### 🏢 关于简仪科技
专业的PXI模块化测控解决方案提供商
- 官网: https://www.jytek.com
- 邮箱: info@jytek.com
```

6. 点击 "Publish release"

## 🌟 优化GitHub仓库

### 1. 添加仓库标签 (Topics)
在仓库主页点击设置图标，添加标签：
- `pxi`
- `ai`
- `flask`
- `python`
- `automation`
- `instrumentation`
- `jytek`
- `measurement`

### 2. 设置仓库描述
```
🚀 锐视测控平台 - 基于AI技术的智能化PXI测控解决方案平台 | AI-Powered PXI Control Platform
```

### 3. 添加网站链接
如果有在线演示，在仓库设置中添加网站链接。

### 4. 启用GitHub Pages (可选)
如果想要托管静态演示页面：
1. 进入仓库设置
2. 找到 "Pages" 部分
3. 选择源分支 (通常是main)
4. 选择文件夹 (/ 或 /docs)

## 📢 推广和分享

### 1. 社交媒体分享
- 在LinkedIn、Twitter等平台分享项目
- 使用相关标签: #PXI #AI #OpenSource #JYTEK

### 2. 技术社区
- 在相关技术论坛分享
- 提交到awesome列表
- 参与开源项目展示

### 3. 文档和博客
- 写技术博客介绍项目
- 制作使用教程视频
- 参与技术会议演讲

## 🔄 持续维护

### 1. 定期更新
- 修复bug和安全问题
- 添加新功能
- 更新依赖包

### 2. 社区互动
- 及时回复Issues
- 审查Pull Requests
- 维护项目文档

### 3. 版本管理
- 遵循语义化版本控制
- 维护CHANGELOG
- 定期发布新版本

## 📞 获取帮助

如果在发布过程中遇到问题：

1. **GitHub官方文档**: https://docs.github.com
2. **Git教程**: https://git-scm.com/docs
3. **简仪科技支持**: info@jytek.com

---

**🌟 祝您发布成功！让我们一起构建更好的PXI测控生态系统！**
