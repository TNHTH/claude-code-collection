---
name: workflow-state
description: Workflow状态跟踪协议
---

# Workflow状态跟踪协议

> **版本**: v1.0
> **生效日期**: 2026-01-30
> **用途**: Agent协作自动化的状态管理和持久化

---

## 核心概念

### 状态机流转

```yaml
完整开发流水线状态机:

States:
  IDLE:       初始状态
  PRODUCT:    需求分析（Product Agent）
  ARCHITECT:  架构设计（Architect Agent）
  DEVELOP:    开发实现（Backend/Frontend Agent）
  REVIEW:     代码审查（Code-Reviewer Agent）
  DOCS:       文档编写（Docs Agent）
  DEVOPS:     部署运维（DevOps Agent）
  DONE:       完成

Transitions:
  IDLE → PRODUCT: 用户说"新建项目"
  PRODUCT → ARCHITECT: Product输出[[AGENT_COMPLETE]]
  ARCHITECT → DEVELOP: Architect输出[[AGENT_COMPLETE]]
  DEVELOP → REVIEW: Backend/Frontend输出[[AGENT_COMPLETE]]
  REVIEW → DOCS: Code-Reviewer输出passed状态
  REVIEW → DEVELOP: Code-Reviewer输出failed状态
  DOCS → DEVOPS: Docs输出[[AGENT_COMPLETE]]
  DEVOPS → DONE: DevOps输出[[AGENT_COMPLETE]]

User Overrides（用户可随时覆盖）:
  用户说"跳过review" → REVIEW → DOCS
  用户说"回到架构" → * → ARCHITECT
  用户说"暂停" → * → PAUSED
```

---

## 完成标记格式

### Agent输出协议

每个Agent完成任务后，必须输出以下标记：

```markdown
[[AGENT_COMPLETE]]
[[CURRENT_STATE: <当前阶段>]]
[[NEXT_STATE: <下一阶段>]]
[[AUTO_TRIGGER: <true/false>]]
[[WORKFLOW_STATE_UPDATE]]
{
  "current": "<当前阶段>",
  "status": "<completed/failed/passed>",
  "output_anchor": "[[<锚点名>]]",
  "completed_at": "YYYY-MM-DD HH:MM:SS"
}
[[WORKFLOW_STATE_UPDATE_END]]
```

### 示例

**Product Agent完成**:
```markdown
[[AGENT_COMPLETE]]
[[CURRENT_STATE: PRODUCT]]
[[NEXT_STATE: ARCHITECT]]
[[AUTO_TRIGGER: true]]
[[WORKFLOW_STATE_UPDATE]]
{
  "current": "PRODUCT",
  "status": "completed",
  "output_anchor": "[[ATOMIC_PRD]]",
  "completed_at": "2026-01-30 16:45:00"
}
[[WORKFLOW_STATE_UPDATE_END]]
```

**Code-Reviewer Agent完成（通过）**:
```markdown
[[AGENT_COMPLETE]]
[[CURRENT_STATE: REVIEW]]
[[NEXT_STATE: DOCS]]
[[AUTO_TRIGGER: true]]
[[WORKFLOW_STATE_UPDATE]]
{
  "current": "REVIEW",
  "status": "passed",
  "critical_issues": 0,
  "major_issues": 0,
  "minor_issues": 3,
  "completed_at": "2026-01-30 17:30:00"
}
[[WORKFLOW_STATE_UPDATE_END]]
```

**Code-Reviewer Agent完成（不通过）**:
```markdown
[[AGENT_COMPLETE]]
[[CURRENT_STATE: REVIEW]]
[[NEXT_STATE: DEVELOP]]
[[AUTO_TRIGGER: true]]
[[WORKFLOW_STATE_UPDATE]]
{
  "current": "REVIEW",
  "status": "failed",
  "critical_issues": 2,
  "requires_fix": true,
  "fix_agent": "backend",
  "completed_at": "2026-01-30 17:30:00"
}
[[WORKFLOW_STATE_UPDATE_END]]
```

---

## 状态持久化

### 文件位置

```
.claude-temp/workflow-state-{项目名}.json
```

### 状态文件格式

```json
{
  "project_name": "待办事项应用",
  "started_at": "2026-01-30 16:00:00",
  "last_updated": "2026-01-30 17:30:00",
  "current_state": "REVIEW",
  "previous_state": "DEVELOP",
  "next_state": "DOCS",

  "stages": {
    "PRODUCT": {
      "status": "completed",
      "agent": "Product Agent",
      "output_anchor": "[[ATOMIC_PRD]]",
      "completed_at": "2026-01-30 16:15:00",
      "duration_minutes": 15
    },
    "ARCHITECT": {
      "status": "completed",
      "agent": "Architect Agent",
      "output_anchor": "[[ARCHITECTURE_DESIGN]]",
      "completed_at": "2026-01-30 16:45:00",
      "duration_minutes": 30
    },
    "DEVELOP": {
      "status": "completed",
      "agent": "Backend Agent",
      "output_files": [
        "src/controllers/userController.ts",
        "src/services/userService.ts"
      ],
      "completed_at": "2026-01-30 17:15:00",
      "duration_minutes": 30
    },
    "REVIEW": {
      "status": "in_progress",
      "agent": "Code-Reviewer Agent",
      "started_at": "2026-01-30 17:30:00"
    }
  },

  "anchors": {
    "PROJECT_GENESIS": "从对话开头到[[PROJECT_GENESIS_END]]",
    "ATOMIC_PRD": "从[[ATOMIC_PRD]]到[[ATOMIC_PRD_END]]",
    "ARCHITECTURE_DESIGN": "从[[ARCHITECTURE_DESIGN]]到[[ARCHITECTURE_DESIGN_END]]"
  },

  "metadata": {
    "total_duration_minutes": 90,
    "auto_trigger_enabled": true,
    "user_interrupted": false
  }
}
```

---

## 自动触发逻辑

### 触发检测算法（主AI执行）

```python
def detect_agent_transition(conversation_history):
    """
    主AI在每次Agent输出后执行
    """
    # 1. 检测完成标记
    last_message = conversation_history[-1]

    if "[[AGENT_COMPLETE]]" in last_message:
        current_state = extract_state(last_message)
        next_state = extract_next_state(last_message)
        auto_trigger = extract_flag(last_message)  # true/false

        # 2. 判断是否自动触发
        if auto_trigger:
            # 3. 等待用户干预（检测下一轮用户输入）
            user_input = wait_for_user_input(timeout=0)

            if not user_input:
                # 4. 用户没有输入，自动触发下一个Agent
                trigger_agent(next_state, context={
                    "anchors": extract_anchors(last_message),
                    "history": conversation_history,
                    "current_state": current_state,
                    "workflow_state": load_workflow_state()
                })

                return "AUTO_TRIGGERED"

    return "MANUAL_TRIGGER_REQUIRED"
```

### 用户干预机制

**规则**: 任何用户输入都会取消自动触发

```yaml
用户在Agent输出后输入任何内容 → 自动触发取消

取消后显示:
  "⏸️ 自动触发已取消
   当前阶段: PRODUCT
   下一阶段: ARCHITECT
   继续请说: 'architect开始' / '继续' / 'next' / '自动'"
```

---

## 用户控制命令

### 基本命令

```yaml
"继续" / "next" / "自动":
  → 恢复自动触发

"暂停" / "stop":
  → 暂停自动触发
  → 设置 AUTO_TRIGGER = false

"跳过[阶段名]":
  → 跳过当前或指定阶段
  → 示例: "跳过review" → REVIEW → DOCS

"回到[阶段名]":
  → 回退到指定阶段
  → 示例: "回到架构" → * → ARCHITECT
  → 示例: "回到需求" → * → PRODUCT

"状态" / "进度":
  → 显示当前工作流状态
  → 输出WORKFLOW_STATE和TASK_LIST

"重置":
  → 清除所有锚点和状态
  → 回到IDLE状态
```

### 高级命令

```yaml
"修复":
  → 在REVIEW失败后，回到DEVELOP修复问题

"强制[阶段名]":
  → 强制进入指定阶段，跳过中间阶段
  → 示例: "强制review" → 直接进入代码审查
```

---

## 状态显示UI

### 进度显示模板

```markdown
---
## 📊 项目进度

**当前阶段**: 🔄 代码审查（Code-Reviewer Agent）
**项目名称**: 待办事项应用
**开始时间**: 2026-01-30 16:00
**已用时**: 90分钟

**已完成**:
  ✅ 需求分析（Product Agent） - 16:15 (15分钟)
  ✅ 架构设计（Architect Agent） - 16:45 (30分钟)
  ✅ 后端开发（Backend Agent） - 17:15 (30分钟)

**当前**:
  🔄 代码审查（Code-Reviewer Agent） - 进行中 (15分钟)

**待完成**:
  ⏸️ 文档编写（Docs Agent）
  ⏸️ 部署运维（DevOps Agent）

**控制**:
- 暂停自动触发: "暂停"
- 跳过当前阶段: "跳过"
- 查看详细状态: "状态"
- 回退到上一阶段: "回到[阶段名]"

---
```

---

## 错误处理

### Agent调用失败

```yaml
检测到Agent调用失败 → 记录错误 → 询问用户

示例输出:
  "⚠️ Architect Agent调用失败
   错误: 超时
   选项:
   1. 重试
   2. 跳过（进入下一阶段）
   3. 手动调用
   请选择: [1] 重试  [2] 跳过  [3] 手动调用"
```

### 状态恢复

```yaml
对话中断后恢复:

1. 检测到.claude-temp/workflow-state-{项目名}.json
2. 加载状态文件
3. 显示恢复提示:
   "💡 检测到未完成的项目: {项目名}
    上次进度: {current_state}
    是否继续？[是/否]"
4. 用户确认 → 恢复状态和锚点
5. 继续执行
```

---

## 实现优先级

### Phase 1: 核心自动触发（✅ 已完成）

- ✅ 7个Agent添加完成标记
- ✅ 定义自动触发协议
- ✅ 定义状态流转规则

### Phase 2: 状态持久化（待主AI实现）

- ⏳ 创建workflow-state.json文件
- ⏳ 实现状态保存/加载逻辑
- ⏳ 实现状态恢复机制

### Phase 3: Code-Reviewer自动触发（✅ 已完成）

- ✅ 定义review通过/不通过流转
- ✅ 定义修复循环workflow

### Phase 4: 用户控制命令（待主AI实现）

- ⏳ 实现"暂停/继续/跳过/回到"命令
- ⏳ 实现状态显示UI
- ⏳ 完善错误处理

---

## 向后兼容

### 保留手动触发

```yaml
自动触发 != 强制触发

所有现有的手动触发方式仍然有效:
  - 用户说 "architect开始" → ✅ 仍然工作
  - 用户说 "review" → ✅ 仍然工作

自动触发只是"默认行为"，用户随时可以覆盖
```

---

## 测试用例

### Test Case 1: 完整自动流程

```yaml
输入: "新建一个待办事项应用"
预期:
  1. Product自动触发
  2. Product完成 → 输出[[AGENT_COMPLETE]]
  3. 用户无输入 → Architect自动触发
  4. Architect完成 → 输出[[AGENT_COMPLETE]]
  5. 用户无输入 → Backend自动触发
  6. Backend完成 → 输出[[AGENT_COMPLETE]]
  7. 用户无输入 → Code-Reviewer自动触发
```

### Test Case 2: 用户中断

```yaml
输入: "新建项目" → [Product完成] → "等等"
预期:
  1. Product输出[[AGENT_COMPLETE]]
  2. 检测到用户输入"等等"
  3. 自动触发取消
  4. 显示状态和控制选项
```

### Test Case 3: Review阻断循环

```yaml
输入: [Backend完成] → [Code-Reviewer发现严重问题]
预期:
  1. Code-Reviewer输出status: "failed"
  2. NEXT_STATE: "DEVELOP"
  3. 自动触发Backend修复
  4. 修复后 → 重新触发Code-Reviewer
  5. Review通过 → 触发Docs
```

---

## 关键设计决策

### 为什么不用"等待3秒"？

```yaml
问题: 3秒等待不稳定
  - AI响应时间不可控
  - 可能导致用户体验差

改进: 检测用户输入
  - Agent输出后，检测下一轮用户输入
  - 如果输入不是控制命令 → 自动触发
  - 如果用户明确取消 → 手动触发
```

### 为什么需要状态持久化？

```yaml
问题: 对话中断后无法恢复
  - 上下文限制导致对话被压缩
  - 用户需要重新开始

解决: workflow-state.json
  - 保存每个阶段的输出
  - 保存锚点位置
  - 对话中断后可以恢复
```

---

**版本**: v1.0
**最后更新**: 2026-01-30
**维护者**: Claude Code AI Assistant
