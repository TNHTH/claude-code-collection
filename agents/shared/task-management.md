---
name: task-management
description: 任务管理规范
---

# 任务管理规范 (Todo Management)

**版本**: v1.0
**更新日期**: 2026-01-12
**适用于**: 所有Agent

---

## 🎯 核心原则

### 何时使用 TodoWrite

**✅ 必须使用**：
1. **复杂多步骤任务**（3个以上步骤）
2. **用户明确要求多个任务**
3. **需要向用户展示进度**
4. **接收到新的重要指令**

**示例**：
```
用户：实现用户注册、登录、密码重置功能

✅ 应该创建todo：
- 任务分解为3个主要功能
- 每个功能需要多个步骤
- 用户可以看到整体进度
```

---

### ❌ 不要使用 TodoWrite

**1. 单个简单任务**
```
用户：帮我读取这个文件

❌ 不要创建todo：
[{"content": "读取文件", "status": "in_progress"}]

✅ 直接读取文件即可
```

**2. 操作性任务（非真正的工作任务）**
```
❌ 绝对不要放入todo：
- "Lint代码"（这是操作，不是任务）
- "运行测试"（这是操作，不是任务）
- "搜索代码库"（这是收集信息，不是任务）
- "检查错误"（这是验证，不是任务）

✅ 应该放入todo的是：
- "实现用户认证功能"（真正的任务）
- "设计数据库Schema"（真正的任务）
- "创建API端点"（真正的任务）
```

**3. 可以直接完成的操作**
```
用户：运行npm install

❌ 不要创建todo

✅ 直接执行即可
```

**4. 纯信息查询**
```
用户：这个函数是做什么的？

❌ 不要创建todo

✅ 直接查询并回答
```

---

## 📊 任务状态管理

### 任务状态
```javascript
{
  "content": "实现用户注册API",
  "status": "pending"  // pending | in_progress | completed | cancelled
}
```

### 状态转换规则

```
pending → in_progress → completed
   ↓
cancelled (任意时刻可取消)
```

### 关键规则

**1. 同时只有1个任务 in_progress**
```javascript
❌ 错误：
[
  {id: "1", "status": "in_progress", content: "任务1"},
  {id: "2", "status": "in_progress", content: "任务2"}
]

✅ 正确：
[
  {id: "1", "status": "in_progress", content: "任务1"},
  {id: "2", "status": "pending", content: "任务2"},
  {id: "3", "status": "pending", content: "任务3"}
]
```

**2. 完成后立即标记**
```javascript
// 完成任务1后
[
  {id: "1", "status": "completed", content: "任务1"},
  {id: "2", "status": "in_progress", content: "任务2"},  // 立即开始任务2
  {id: "3", "status": "pending", content: "任务3"}
]

❌ 不要批量标记：
// 不要等所有任务完成后再一起标记
```

**3. 动态调整任务列表**
```javascript
// 如果发现新任务，立即添加
[
  {id: "1", "status": "completed", content: "任务1"},
  {id: "2", "status": "in_progress", content: "任务2"},
  {id: "3", "status": "pending", content: "任务3"},
  {id: "4", "status": "pending", content: "新发现的任务"}
]
```

---

## 🔥 实战示例

### 示例1: 多功能开发

**用户需求**：
```
实现一个博客系统，包括：
1. 用户注册和登录
2. 文章的增删改查
3. 评论功能
```

**✅ 正确的Todo使用**：
```javascript
// 第1次TodoWrite - 任务分解
[
  {id: "1", "status": "in_progress", content: "设计数据库Schema"},
  {id: "2", "status": "pending", content: "实现用户认证API"},
  {id: "3", "status": "pending", content: "实现文章CRUD API"},
  {id: "4", "status": "pending", content: "实现评论功能"},
  {id: "5", "status": "pending", content: "创建前端页面"}
]

// 完成任务1后
[
  {id: "1", "status": "completed", content: "设计数据库Schema"},
  {id: "2", "status": "in_progress", content: "实现用户认证API"},
  {id: "3", "status": "pending", content: "实现文章CRUD API"},
  {id: "4", "status": "pending", content: "实现评论功能"},
  {id: "5", "status": "pending", content: "创建前端页面"}
]
```

### 示例2: 不应该使用Todo的场景

**用户需求**：
```
帮我检查一下这段代码有没有问题
```

**❌ 错误的Todo使用**：
```javascript
[
  {id: "1", "status": "in_progress", content: "检查代码"}
]
// 这是单个简单任务，不需要todo
```

**✅ 正确的做法**：
```javascript
// 直接读取代码、分析、给出建议
// 不使用TodoWrite
```

---

## 🎯 任务分解指南

### 如何分解复杂任务

**原则**：每个任务应该是独立、可测试、可验证的

**示例**：
```
原始任务：实现一个博客系统

❌ 太粗糙：
[{"content": "实现博客"}]

❌ 太细碎：
[
  {"content": "创建项目文件夹"},
  {"content": "初始化npm"},
  {"content": "安装依赖"},
  {"content": "创建第一个文件"},
  ...
]

✅ 合理分解：
[
  {"content": "设计数据库Schema"},
  {"content": "实现后端API"},
  {"content": "实现前端页面"},
  {"content": "集成测试"}
]
```

### 任务粒度标准

**合适的粒度**：
- 每个任务1-4小时完成
- 可以独立测试
- 有明确的完成标准
- 依赖关系清晰

---

## 📋 任务管理最佳实践

### 1. 任务命名规范

**✅ 好的任务名称**：
```javascript
{"content": "设计用户认证API"}
{"content": "实现登录功能"}
{"content": "编写API文档"}
```

**❌ 不好的任务名称**：
```javascript
{"content": "做登录"}  // 太模糊
{"content": "工作"}    // 无意义
{"content": "代码"}    // 不具体
```

### 2. 任务完成标准

每个任务应该有明确的完成标准：
```
任务："实现用户注册API"

完成标准：
- ✅ POST /api/auth/register 端点创建
- ✅ 输入验证实现
- ✅ 密码哈希实现
- ✅ 错误处理完善
- ✅ 测试通过
```

### 3. 动态调整

```javascript
// 如果发现任务需要拆分
原任务：{"content": "实现用户系统"}

// 拆分为：
[
  {"content": "实现用户注册"},
  {"content": "实现用户登录"},
  {"content": "实现密码重置"}
]

// 如果发现任务不再需要
[
  {id: "3", "status": "cancelled", content": "实现短信通知"}
]
```

---

## ⚠️ 常见错误

### 错误1: 过度使用Todo
```
❌ 错误：
用户：读取文件A

Agent：创建todo "读取文件A"
      读取文件A
      标记完成

✅ 正确：
直接读取文件A
```

### 错误2: 任务不明确
```
❌ 错误：
{"content": "后端"}

✅ 正确：
{"content": "实现用户注册API"}
```

### 错误3: 同时多个任务 in_progress
```
❌ 错误：
[
  {status: "in_progress", content: "任务1"},
  {status: "in_progress", content: "任务2"}
]

✅ 正确：
[
  {status: "in_progress", content: "任务1"},
  {status: "pending", content: "任务2"}
]
```

### 错误4: 批量标记完成
```
❌ 错误：
// 做完所有任务后一次性更新
[all tasks completed]

✅ 正确：
// 完成一个立即标记一个
task1 completed → update
task2 completed → update
task3 completed → update
```

---

## 🎯 总结

### 使用TodoWrite的时机
- ✅ 复杂任务（3+步骤）
- ✅ 多任务并行
- ✅ 需要展示进度
- ✅ 用户明确要求

### 不使用TodoWrite的时机
- ❌ 单个简单任务
- ❌ 操作性任务（lint, test, search）
- ❌ 信息查询
- ❌ 可以直接完成的操作

### 核心规则
1. **同时只有1个任务 in_progress**
2. **完成后立即标记为 completed**
3. **任务命名要明确具体**
4. **任务粒度要合适**（1-4小时）
5. **动态调整，灵活应变**

---

**记住**：TodoWrite是任务管理工具，不是操作日志。

**目标**：帮助用户理解进度，而不是记录每个操作。
