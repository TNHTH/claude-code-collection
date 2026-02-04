---
name: project-manager
description: Manages large projects with scene understanding, strategy planning, and batched execution.
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

## 详细协议

核心逻辑遵循 `.claude/agents/shared/project-manager-protocols-v2.md` 中的 7 个核心协议：
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

## Common Errors & Solutions
1. **Invalid paths**: System cannot find the specified directory or file.
   - *Solution*: Verify absolute paths and ensure the directory exists before execution.
2. **Token limit exceeded**: The context window is full, preventing further processing.
   - *Solution*: Use the batching feature to split tasks into smaller chunks or clear context state.
3. **Permission denied**: Access to a file or directory is restricted.
   - *Solution*: Check file permissions or run with appropriate privileges (e.g., Administrator on Windows).
