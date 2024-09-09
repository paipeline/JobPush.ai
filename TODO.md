# 项目功能清单
--------- v1 ---------
## 1. 数据持久化存储
**描述**: 将爬取的各类别工作数据持久化存储到PostgreSQL数据库中。
**任务**:
- [ ] 设计数据库模式
- [ ] 实现CSV到PostgreSQL的数据导入脚本
- [ ] 设置定期数据更新机制
- [ ] 实现数据查询API
**负责人**:
**状态**:
**截止日期**:

## 2. 用户简历管理系统
**描述**: 通过微信公众号实现用户简历的私密上传、存储和管理。

### 2.1 微信公众号设置
- [ ] 注册微信公众号
- [ ] 配置公众号基本信息
- [ ] 开发公众号菜单和基本功能
**负责人**:
**状态**:
**截止日期**:

### 2.2 用户数据持久化
- [ ] 设计用户数据模型
- [ ] 实现用户认证和授权系统
- [ ] 开发用户数据CRUD操作API
- [ ] 实现数据加密存储
**负责人**:
**状态**:
**截止日期**:

### 2.3 简历上传和OCR服务
- [ ] 开发简历上传功能
- [ ] 集成OCR服务进行简历文本提取
- [ ] 实现简历数据结构化存储
- [ ] 开发简历预览和编辑功能
**负责人**:
**状态**:
**截止日期**:

## 3. AI驱动的简历-工作匹配系统
**描述**: 使用RAG(检索增强生成)系统实现简历与工作描述的智能匹配。
**任务**:
- [ ] 设计和实现向量数据库
- [ ] 开发文本嵌入模型
- [ ] 实现相似度搜索算法
- [ ] 开发匹配结果排序和过滤机制
- [ ] 集成大语言模型进行结果优化
**负责人**:
**状态**:
**截止日期**:


--------- v2 ---------
## 4. 前端网站开发
**描述**: 开发一个用户友好的前端网站,展示匹配结果和管理用户账户。
**任务**:
- [ ] 设计网站UI/UX
- [ ] 实现用户注册和登录功能
- [ ] 开发工作搜索和浏览界面
- [ ] 实现简历上传和管理界面
- [ ] 开发匹配结果展示页面
- [ ] 实现响应式设计,确保移动端兼容性
**负责人**:
**状态**:
**截止日期**:

## 5. 系统集成和测试
**描述**: 整合所有组件并进行全面测试。
**任务**:
- [ ] 集成所有后端服务
- [ ] 连接前端与后端API
- [ ] 进行单元测试和集成测试
- [ ] 执行用户验收测试
- [ ] 进行性能和安全测试
**负责人**:
**状态**:
**截止日期**:

## 6. 部署服务到AWS Lambda和维护
**描述**: 将系统部署到生产环境并制定维护计划。
**任务**:
- [ ] 设置生产服务器环境
- [ ] 配置CI/CD管道
- [ ] 实施监控和日志系统
- [ ] 制定备份和恢复策略
- [ ] 编写系统文档和用户手册
**负责人**:
**状态**:
**截止日期**: