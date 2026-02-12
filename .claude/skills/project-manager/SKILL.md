---
name: project-manager
description: |
  项目管理工具。触发词：项目管理、任务分解、进度追踪、批量执行、复杂项目、多阶段任务。
  Manages large projects with scene understanding, strategy planning, and batched execution.
version: 1.0
author: Claude
---

> **Skill名称**: project-manager
> **版本**: v1.0
> **创建时间**: 2026-02-03
> **适用场景**: 大型项目管理（100+文件），分批执行，断点续传

## Skill描述

这是一个智能项目管理工具，负责管理和协调大型项目任务，通过场景理解、意图理解、策略规划、分批执行、断点续传解决复杂项目管理和上下文限制问题。

**核心能力**:
- **场景理解**: 识别项目类型（深度学习/Web/CLI/数据分析），确定文件规模。
- **项目分析**: 自动扫描文件结构，生成 `project-index.md` 索引。
- **策略规划**: 根据项目现状和用户目标制定执行计划。
- **分批执行**: 动态调整批次大小，实时监控 Token 使用，支持大体量任务。
- **进度管理**: 自动保存执行状态到 `progress.md`，支持中断恢复。
- **总结索引**: 生成项目总结和导航文档。

## 使用方法

**触发指令**:
- "分析项目"
- "整理文件"
- "项目文档"
- "搭建项目"
- "优化项目"

**带参数使用**:
- `/skill project-manager`

## 工作流程

1.  **场景理解**: 识别项目类型，确定规模。
2.  **意图理解**: 明确用户任务（分析/创建/修改）。
3.  **项目分析**: 扫描并生成索引。
4.  **策略规划**: 制定分步执行计划。
5.  **任务执行**:
    *   分批处理文件。
    *   执行具体任务（代码分析、重构、文档生成等）。
    *   实时更新 `progress.md`。
6.  **总结输出**: 生成项目总结报告。

## 执行铁律 (The Iron Law of Execution)

> **⚠️ 绝对禁止一次性执行超过 10 个文件的变更而没有中间验证。**
> **Never execute >10 file changes without verification.**

### 分批执行协议 (Batched Execution Protocol)

当任务涉及多个文件或步骤时，**必须**强制执行以下分批逻辑：

1.  **分批 (Batching)**: 将任务拆分为每批 5-10 个文件的微任务。
2.  **存盘 (Check-pointing)**: 每完成一批，**立即**更新 `progress.md`。
3.  **验证 (Validation)**: 在开始下一批之前，必须验证上一批是否成功（如：文件是否存在、语法是否正确）。
    *   **成功** -> 继续下一批。
    *   **失败** -> **停止**。修复问题或回滚，禁止盲目继续。

**❌ 错误做法**: "我将一次性为您创建所有 50 个组件文件..." (这会导致上下文溢出或错误的累积)。
**✅ 正确做法**: "任务涉及 50 个文件。我将分为 5 批执行。现在开始第 1 批 (1-10)..."

---

## 详细协议

核心逻辑遵循以下 7 个核心协议：
1.  场景理解协议
2.  意图理解协议
3.  项目分析协议
4.  策略规划协议
5.  任务执行协议
6.  进度管理协议
7.  增量更新协议

## 状态文件

-   **索引文件**: `.claude-temp/{project-name}/project-index.md`
-   **进度文件**: `.claude-temp/{project-name}/progress.md`

## 错误处理

-   **Token 超限**: 自动触发保存进度并清理上下文。
-   **任务中断**: 下次启动时读取 `progress.md` 询问是否继续。

## PRD 模板（需求分析）

当用户需要需求分析、PRD、用户故事时，使用以下结构：

### 输出格式：`product-requirements.md`

```markdown
## Problem Statement
要解决什么问题

## User Stories
As a [role], I want [feature], so that [benefit]

## Acceptance Criteria (Gherkin)
Given [前置条件]
When [用户操作]
Then [期望结果]

## Non-Functional Requirements
性能、安全等要求

## Scope Boundary
明确"不做什么"
```

### 需求分析流程

1. **苏格拉底式提问** — 澄清模糊需求
2. **MECE拆解** — 功能模块不重不漏
3. **用户故事映射** — As a / I want / So that
4. **Gherkin验收标准** — Given / When / Then
5. **范围控制** — 明确"不做什么"，防止功能蔓延

## Common Errors & Solutions
1. **Invalid paths**: System cannot find the specified directory or file.
   - *Solution*: Verify absolute paths and ensure the directory exists before execution.
2. **Token limit exceeded**: The context window is full, preventing further processing.
   - *Solution*: Use the batching feature to split tasks into smaller chunks or clear context state.
3. **Permission denied**: Access to a file or directory is restricted.
   - *Solution*: Check file permissions or run with appropriate privileges (e.g., Administrator on Windows).
