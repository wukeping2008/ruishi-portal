# 贡献指南 (Contributing Guide)

感谢您对锐视测控平台的关注！我们欢迎所有形式的贡献，包括但不限于：

- 🐛 Bug 报告
- 💡 功能建议
- 📝 文档改进
- 🔧 代码贡献
- 🌍 翻译支持

## 🚀 快速开始

### 开发环境设置

1. **Fork 项目**
   ```bash
   # 在 GitHub 上 Fork 项目到您的账户
   ```

2. **克隆项目**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ruishi-portal.git
   cd ruishi-portal
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置开发环境**
   ```bash
   # 复制配置文件模板
   cp src/config.json.example src/config.json
   # 编辑配置文件，添加您的 AI API 密钥
   ```

5. **启动开发服务器**
   ```bash
   cd src
   python main.py
   ```

## 📋 开发规范

### 代码风格

#### Python 代码
- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范
- 使用 [Black](https://black.readthedocs.io/) 进行代码格式化
- 函数和类需要有详细的文档字符串

```python
def example_function(param1: str, param2: int) -> dict:
    """
    示例函数说明
    
    Args:
        param1: 参数1说明
        param2: 参数2说明
        
    Returns:
        返回值说明
    """
    pass
```

#### JavaScript 代码
- 使用 ES6+ 语法
- 遵循 [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- 使用有意义的变量和函数名
- 添加必要的注释

```javascript
/**
 * 示例函数说明
 * @param {string} param1 - 参数1说明
 * @param {number} param2 - 参数2说明
 * @returns {Object} 返回值说明
 */
function exampleFunction(param1, param2) {
    // 实现逻辑
}
```

### 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### 提交类型
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

#### 示例
```bash
feat(ai): 添加新的AI提供商支持
fix(ui): 修复移动端响应式布局问题
docs(readme): 更新安装指南
```

## 🔄 贡献流程

### 1. 创建 Issue
在开始开发之前，请先创建一个 Issue 来描述：
- 要解决的问题
- 建议的解决方案
- 相关的技术细节

### 2. 创建分支
```bash
# 从 main 分支创建新分支
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

### 3. 开发和测试
- 编写代码
- 添加或更新测试
- 确保所有测试通过
- 更新相关文档

### 4. 提交代码
```bash
git add .
git commit -m "feat: 添加新功能描述"
git push origin feature/your-feature-name
```

### 5. 创建 Pull Request
- 在 GitHub 上创建 Pull Request
- 填写详细的 PR 描述
- 关联相关的 Issue
- 等待代码审查

## 🧪 测试指南

### 运行测试
```bash
# 运行所有测试
python -m pytest

# 运行特定测试文件
python -m pytest tests/test_llm_models.py

# 运行测试并生成覆盖率报告
python -m pytest --cov=src
```

### 编写测试
- 为新功能编写单元测试
- 确保测试覆盖率不低于 80%
- 测试文件命名规范：`test_*.py`

```python
import pytest
from src.models.llm_models import LLMManager

def test_llm_manager_initialization():
    """测试 LLM 管理器初始化"""
    manager = LLMManager()
    assert manager is not None
    assert len(manager.providers) == 0
```

## 📚 文档贡献

### 文档类型
- **README.md**: 项目介绍和快速开始
- **API 文档**: API 接口说明
- **用户指南**: 详细的使用说明
- **开发文档**: 架构和开发指南

### 文档规范
- 使用 Markdown 格式
- 提供中英文双语版本
- 包含代码示例
- 保持文档与代码同步

## 🌍 国际化贡献

### 添加新语言支持
1. 在 `src/static/js/i18n.js` 中添加新语言的翻译
2. 更新语言选择器
3. 测试所有页面的翻译效果

### 翻译指南
- 保持技术术语的准确性
- 考虑目标语言的文化背景
- 保持界面文本的简洁性

## 🐛 Bug 报告

### 报告 Bug 时请包含：
- **环境信息**: 操作系统、Python 版本、浏览器版本
- **重现步骤**: 详细的操作步骤
- **期望行为**: 您期望发生什么
- **实际行为**: 实际发生了什么
- **错误信息**: 完整的错误日志
- **截图**: 如果适用的话

### Bug 报告模板
```markdown
## Bug 描述
简要描述遇到的问题

## 环境信息
- 操作系统: [例如 macOS 12.0]
- Python 版本: [例如 3.9.7]
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

## 错误信息
```
粘贴完整的错误日志
```

## 截图
如果适用，请添加截图来帮助解释问题
```

## 💡 功能建议

### 建议新功能时请包含：
- **功能描述**: 详细描述建议的功能
- **使用场景**: 什么情况下会用到这个功能
- **实现建议**: 如果有的话，提供实现思路
- **优先级**: 评估功能的重要性

## 📞 联系方式

如果您有任何问题或需要帮助，可以通过以下方式联系我们：

- **GitHub Issues**: [创建 Issue](https://github.com/jytek/ruishi-portal/issues)
- **邮箱**: support@jytek.com
- **官网**: https://www.jytek.com

## 🙏 致谢

感谢所有为锐视测控平台做出贡献的开发者！

### 贡献者列表
<!-- 这里会自动更新贡献者列表 -->

---

再次感谢您的贡献！让我们一起打造更好的 PXI 测控解决方案！ 🚀
