# GitHub 开源发布指南

本文档提供了将锐视测控平台发布到GitHub的完整步骤指南。

## 📋 发布前检查清单

### ✅ 必需文件
- [x] `README.md` - 项目介绍和使用指南
- [x] `LICENSE` - MIT开源许可证
- [x] `CONTRIBUTING.md` - 贡献指南
- [x] `CHANGELOG.md` - 版本更新记录
- [x] `.gitignore` - Git忽略文件配置
- [x] `requirements.txt` - Python依赖列表
- [x] `src/config.json.example` - 配置文件模板

### ✅ 代码准备
- [x] 移除敏感信息 (API密钥已移至config.json.example)
- [x] 代码注释完整
- [x] 文档齐全
- [x] 项目结构清晰

## 🚀 GitHub发布步骤

### 1. 创建GitHub仓库

1. **登录GitHub**
   - 访问 https://github.com
   - 登录您的GitHub账户

2. **创建新仓库**
   ```
   仓库名称: ruishi-portal
   描述: 锐视测控平台 - AI增强的开源PXI测控解决方案
   可见性: Public (公开)
   初始化: 不要初始化README、.gitignore或许可证
   ```

### 2. 本地Git初始化

在项目根目录执行以下命令：

```bash
# 初始化Git仓库
cd ruishi_portal
git init

# 添加所有文件
git add .

# 首次提交
git commit -m "feat: 初始化锐视测控平台开源项目

- 添加多AI集成系统 (Claude, Gemini, Volces Deepseek, Qwen Plus)
- 实现智能模型选择器
- 完整的中英文国际化支持
- 知识库管理系统
- 智能产品配置器
- 响应式Web界面
- 完整的开源文档"

# 添加远程仓库 (替换为您的GitHub用户名)
git remote add origin https://github.com/YOUR_USERNAME/ruishi-portal.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

### 3. 配置GitHub仓库

#### 3.1 仓库设置
1. 进入仓库设置页面
2. 在"General"部分：
   - 确认仓库描述
   - 添加网站链接 (如果有)
   - 添加主题标签：`pxi`, `ai`, `测控`, `python`, `flask`, `javascript`

#### 3.2 创建Release
1. 点击"Releases"
2. 点击"Create a new release"
3. 填写发布信息：
   ```
   Tag version: v1.0.0
   Release title: 锐视测控平台 v1.0.0 - 首次开源发布
   
   描述:
   🎉 **锐视测控平台首次开源发布！**
   
   ## 🌟 主要特性
   - 🤖 多AI集成系统 (支持4个AI提供商)
   - 🧠 智能模型选择器
   - 🌍 完整的中英文国际化
   - 📚 知识库管理系统
   - 🔧 智能产品配置器
   - 📱 响应式Web界面
   
   ## 📊 项目统计
   - 总代码量: 8,833 行
   - 支持语言: Python, JavaScript, HTML
   - AI提供商: 4 个
   - 页面数量: 4 个
   
   ## 🚀 快速开始
   1. 克隆项目: `git clone https://github.com/YOUR_USERNAME/ruishi-portal.git`
   2. 安装依赖: `pip install -r requirements.txt`
   3. 配置API: 复制 `src/config.json.example` 为 `src/config.json`
   4. 启动应用: `cd src && python main.py`
   
   详细使用说明请查看 [README.md](README.md)
   ```

#### 3.3 设置GitHub Pages (可选)
如果要部署静态演示页面：
1. 进入"Settings" > "Pages"
2. 选择源分支
3. 配置自定义域名 (可选)

### 4. 社区功能配置

#### 4.1 Issue模板
创建 `.github/ISSUE_TEMPLATE/` 目录并添加模板：

**Bug报告模板** (`.github/ISSUE_TEMPLATE/bug_report.md`):
```markdown
---
name: Bug报告
about: 创建一个Bug报告来帮助我们改进
title: '[BUG] '
labels: 'bug'
assignees: ''
---

## Bug描述
简要描述遇到的问题

## 环境信息
- 操作系统: [例如 macOS 12.0]
- Python版本: [例如 3.9.7]
- 浏览器: [例如 Chrome 96.0]

## 重现步骤
1. 打开应用
2. 点击 '...'
3. 输入 '...'
4. 看到错误

## 期望行为
描述您期望发生什么

## 实际行为
描述实际发生了什么

## 截图
如果适用，请添加截图
```

**功能请求模板** (`.github/ISSUE_TEMPLATE/feature_request.md`):
```markdown
---
name: 功能请求
about: 建议一个新功能
title: '[FEATURE] '
labels: 'enhancement'
assignees: ''
---

## 功能描述
详细描述建议的功能

## 使用场景
什么情况下会用到这个功能

## 实现建议
如果有的话，提供实现思路

## 优先级
- [ ] 高
- [ ] 中
- [ ] 低
```

#### 4.2 Pull Request模板
创建 `.github/pull_request_template.md`:
```markdown
## 变更描述
简要描述此PR的变更内容

## 变更类型
- [ ] Bug修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 代码重构
- [ ] 性能优化
- [ ] 其他

## 测试
- [ ] 已添加测试用例
- [ ] 所有测试通过
- [ ] 手动测试通过

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 已更新相关文档
- [ ] 已添加必要的注释
- [ ] 无破坏性变更

## 相关Issue
关闭 #(issue编号)
```

### 5. 推广和维护

#### 5.1 README徽章
在README.md中添加状态徽章：
```markdown
![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/ruishi-portal?style=social)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/ruishi-portal?style=social)
![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/ruishi-portal)
![GitHub license](https://img.shields.io/github/license/YOUR_USERNAME/ruishi-portal)
![Python version](https://img.shields.io/badge/Python-3.9+-green?logo=python)
```

#### 5.2 社区建设
- 及时回复Issues和Pull Requests
- 定期更新文档
- 发布新版本时更新CHANGELOG.md
- 参与相关技术社区讨论

## 📝 发布后的维护

### 版本管理
```bash
# 创建新版本标签
git tag -a v1.1.0 -m "Release version 1.1.0"
git push origin v1.1.0

# 在GitHub上创建对应的Release
```

### 持续集成 (可选)
考虑添加GitHub Actions进行自动化：
- 代码质量检查
- 自动化测试
- 自动部署

### 文档维护
- 保持README.md更新
- 及时更新API文档
- 维护CHANGELOG.md

## 🎯 成功指标

### 短期目标 (1-3个月)
- [ ] 获得50+ GitHub Stars
- [ ] 收到第一个Pull Request
- [ ] 建立活跃的Issue讨论

### 中期目标 (3-6个月)
- [ ] 获得200+ GitHub Stars
- [ ] 有5+贡献者
- [ ] 发布3+个版本更新

### 长期目标 (6-12个月)
- [ ] 获得500+ GitHub Stars
- [ ] 建立活跃的开发者社区
- [ ] 成为PXI测控领域的知名开源项目

## 📞 支持

如果在发布过程中遇到问题，可以：
- 查看GitHub官方文档
- 联系项目维护者
- 在相关技术社区寻求帮助

---

**祝您的开源项目发布成功！** 🚀
