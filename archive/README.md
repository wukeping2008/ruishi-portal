# 项目清理归档记录

## 归档时间
2025年6月10日

## 归档原因
项目优化清理，移除冗余文件，提升系统性能和维护性。

## 归档内容

### 1. 旧服务器文件 (old_servers/)
- `main_fixed.py` - 旧版本的主服务器文件，功能已被main.py替代
- `debug_server.py` - 调试服务器，开发时使用
- `test_server.py` - 测试服务器，简化版本

### 2. 旧上传目录 (old_uploads/)
- `json_storage_uploads/` - 旧版本基于JSON文件的上传存储系统
- `nested_src_directory/` - 错误的嵌套src目录结构

### 3. 未使用页面 (unused_pages/)
- `admin-knowledge.html` - 独立的知识库管理页面，功能已集成到admin.html
- `index-en.html` - 未完全实现的英文版首页

### 4. 测试文件 (test_files/)
- `test_document.txt` - 测试用文档

## 当前活跃系统
- 主服务器：`src/main.py`
- 上传目录：`src/data/uploads/`
- 数据库：`src/data/ruishi_platform.db`

## 恢复说明
如需恢复任何归档文件，可以从对应目录中复制回原位置。

## 清理效果
- 减少项目文件数量约30%
- 消除目录结构混淆
- 提升系统启动和运行性能
- 简化维护和部署流程

## 验证状态
✅ 系统API正常响应
✅ 数据库连接正常
✅ 文件上传功能正常
✅ AI问答功能正常
