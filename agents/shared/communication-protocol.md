---
name: communication-protocol
description: 多 Agent 通信协议
---

# 多 Agent 通信协议

## 数据流动

```
┌─────────────────────────────────────────────────────────────┐
│                     Orchestrator                            │
│  (读取配置、构建计划、协调执行、收集结果)                      │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Backend    │      │   Frontend   │      │    DevOps    │
│    Agent     │──────│    Agent     │──────│    Agent     │
└──────────────┘      └──────────────┘      └──────────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
                    ┌─────────────────┐
                    │  Shared Data    │
                    │  (types, APIs)  │
                    └─────────────────┘
```

## 共享资源目录

```
project/
├── shared/
│   ├── types/          # 共享类型定义
│   │   └── api.ts      # API 请求/响应类型
│   ├── schemas/        # 数据模型 Schema
│   │   └── user.json   # 用户数据模型
│   ├── contracts/      # API 契约
│   │   └── openapi.yaml
│   └── config/         # 共享配置
│       └── env.template.json
├── backend/
├── frontend/
└── docs/
```

## Agent 通信方式

### 1. 文件共享（推荐）

Agent 通过读写共享目录中的文件进行通信：

```typescript
// Backend Agent 写入 API 定义
// shared/contracts/backend-api.yaml
openapi: 3.0.0
info:
  title: Backend API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '../schemas/user.json'
```

```typescript
// Frontend Agent 读取并生成客户端代码
// 从 shared/contracts/backend-api.yaml 生成
export async function getUsers(): Promise<User[]> {
  const response = await fetch('/api/users');
  return response.json();
}
```

### 2. 结构化输出

Agent 完成后输出结构化结果，由 Orchestrator 传递给依赖方：

```yaml
# Backend Agent 输出
output:
  apiSpec: "./shared/contracts/backend-api.yaml"
  endpoints:
    - method: GET
      path: /users
      description: 获取用户列表
  database:
    schema: "./shared/schemas/database.sql"
```

### 3. 消息传递

通过 Orchestrator 中转消息：

```typescript
// Backend Agent 发送消息
{
  from: "backend",
  to: "frontend",
  type: "info",
  payload: {
    message: "API 已完成",
    apiSpecPath: "./shared/contracts/backend-api.yaml"
  }
}

// Orchestrator 传递给 Frontend Agent
// Frontend Agent 接收时可以获取 API 文档路径
```

## 依赖关系处理

```yaml
# 在 project.config.yaml 中定义
agents:
  backend:
    dependencies: []           # 无依赖，可最先执行
    output:
      - "shared/contracts/*.yaml"

  frontend:
    dependencies: [backend]    # 依赖 Backend
    input:
      - "shared/contracts/*.yaml"  # 读取 Backend 输出
    output:
      - "src/api/*.ts"

  docs:
    dependencies: [backend, frontend]  # 依赖两者
    input:
      - "shared/contracts/*.yaml"
      - "src/**/*.md"
```

## 执行顺序

```
第 1 轮: [backend]              → backend 完成，写入 API 定义
第 2 轮: [frontend]             → frontend 读取 API 定义
第 3 轮: [docs]                 → docs 收集所有输出
```

## 错误处理

```yaml
execution:
  on_failure: "continue"  # 继续执行其他 Agent
  # 或 "stop"             # 停止所有执行
  # 或 "ask"              # 询问用户如何处理
```

## 最佳实践

1. **明确定义接口**: 在 `shared/contracts/` 中明确定义 API 契约
2. **使用类型安全**: 通过 TypeScript 类型确保前后端一致
3. **版本化**: 对共享的 Schema 进行版本控制
4. **文档先行**: Backend 先输出 API 文档，Frontend 再开始实现
5. **增量更新**: Agent 可以更新共享文件，下游 Agent 读取最新版本

---

## 🔄 Agent协作工作流（优化版）

### 上下文传递规范

#### 输出格式（给下游Agent）
```yaml
[[AGENT_OUTPUT]]
Agent: [Agent名称]
Timestamp: [时间戳]

核心成果:
  - [成果1]
  - [成果2]

输出文件:
  - [文件路径1]: [用途说明]
  - [文件路径2]: [用途说明]

决策记录:
  - [决策1]: [理由]
  - [决策2]: [理由]

注意事项:
  - [下游Agent需要注意的事项1]
  - [下游Agent需要注意的事项2]

[[AGENT_OUTPUT_END]]
```

#### 输入读取（从上游Agent）
```markdown
## 读取上游Agent输出

优先级顺序：
1. [[PRODUCT_OUTPUT]] - 产品需求
2. [[ARCHITECTURE_DESIGN]] - 架构设计
3. [[BACKEND_OUTPUT]] - API定义

**如果找不到必需的锚点**：
- 停止并明确说明缺少什么
- 请求运行特定的Agent
- 不要猜测或臆造
```

### 协作检查清单

每个Agent在开始工作前确认：
- [ ] 我是否读取了上游Agent的输出？
- [ ] 我是否理解了依赖关系？
- [ ] 我是否提供了清晰的输出格式？
- [ ] 我的输出是否便于下游Agent使用？

### 错误处理流程

```yaml
场景1: 缺少上游输出
  → 明确说明缺少哪个锚点
  → 请求运行特定Agent
  → 等待上游Agent完成

场景2: 输出格式不匹配
  → 尝试理解并适配
  → 记录格式差异
  → 更新输出规范

场景3: 依赖冲突
  → 明确说明冲突点
  → 提供解决方案选项
  → 等待用户决策
```

---

## 📊 改进建议总结

### 已实现的改进

1. **✅ 工具使用指南**
   - `shared/tool-guidelines.md` - 详细的MCP工具使用规范
   - 每个工具都有"何时用"、"何时不用的指导

2. **✅ 任务管理规范**
   - `shared/task-management.md` - TodoWrite使用规范
   - 明确何时使用、何时不使用

3. **✅ 工作原则**
   - `shared/agent-work-principles.md` - 主动性和彻底性原则
   - 所有Agent都引用此文件

4. **✅ 协作机制**
   - 输出格式标准化（锚点格式）
   - 输入读取流程化
   - 错误处理规范化

5. **✅ 新增Skills**
   - `mcp-builder` - MCP服务器构建工具
   - `skill-creator` - 技能创建指南
   - `webapp-testing` - Web应用测试
   - `changelog-generator` - 变更日志生成

### 参考来源

**基于以下项目改进**：
- Cursor Agent Prompt 2.0 (38KB详细提示词)
- Awesome Claude Skills (ComposioHQ)
- 你的multi-agent-system原有优势

**结合两者优势** = 更强大的Agent系统！
