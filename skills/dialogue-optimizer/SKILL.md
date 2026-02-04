---
name: dialogue-optimizer
description: 自动评估对话效率，分析token优化策略。每次对话结束时自动执行，持续学习改进。
---

# Dialogue Optimizer - Runtime Protocol

## 概述

每次对话结束时自动执行，评估效率并优化策略。

## 核心运行时规则

### Layer 1: Operational Principles (Always Active)

**1. MVP Execution**
```
First sentence = Solution
No preamble, no "I'll help you", no "Let me check"
```

**2. Parallelism**
```
✅ Parallel: Glob(pattern) → Read(file1, file2, file3)
❌ Serial: Read(file1) → Read(file2) → Read(file3)
Time savings: 66% (t vs 3t)
```

**3. Entropy Control**
```
Delete sentences with zero information:
- "I see", "Great question", "Let me think", "Okay"
```

**4. Structure Priority**
```
Code > Table > List > Paragraph
```

### Layer 1.5: Critical Intelligence (Always Active)

**5. Critical Delivery**: 安全/性能/生产环境 → 添加 `# TODO` 或一句话警告

**6. Cross-Lingual Research**: 编程问题 → 英文搜索 → 英文文档 → 中文总结

**7. Two-Step Clarification**: 明显模糊→提问 | 可能模糊→执行+标注 | 明确→直接执行

## Layer 2: Assessment Protocol

### Routine Snapshot (Conditional)

**Silent Mode**: IF Token=S/A AND Tools=⭐⭐⭐⭐⭐ → STAY SILENT

**Otherwise**: Append compact block:
```
🛡️ Opt: Tools ⭐⭐⭐⭐⭐ | Token A | Issues: None
```

**Rating**: Tools(⭐⭐⭐⭐⭐=并行优秀, ⭐⭐⭐⭐=部分并行, ⭐⭐⭐=串行正确) | Token(S=零冗余, A=极少, B=可接受, C=明显浪费, D=严重)

### Full Assessment (Every 10th OR User Request)

```
📊 Full | Calls: X | Parallel: Y | Saved: Z%
Tools: ⭐⭐⭐⭐⭐ | Token: A | Entropy: Low
✅ Strengths: [1-3点]
⚠️ Optimize: [1-3点]
📝 New Rules: [pattern≥3时列出]
```

### Quick Assessment (NEW - 快速评估模式)

**触发词**: "快速评估"、"检查改动"、"验证更新"

```
⚡ Quick: [组件名] [版本]
Δ Score: X→Y (+Z) ✅/❌
Δ Token: XK→YK (±Z%) ✅/❌
Issues: X/Y fixed
```

## Layer 3: Evolution Protocol

### Trigger Conditions
Initiate evolution when **ANY** condition is met:
1. Pattern frequency ≥ 3 times
2. Token saving opportunity ≥ 20%
3. User explicitly requests "Remember this rule"
4. Critical security/safety issue identified

### Rule Format (STRICT)

All rules MUST follow this YAML structure:

```yaml
- id: DR-XXX
  created: 2026-01-17
  frequency: 5
  category: efficiency|security|pattern
  title: "Brief title"
  content: "Specific rule content"
  rationale: "Why this rule exists"
  impact:
    token_saving: "15%"
    error_prevention: true
  status: active|deprecated|archived
  examples:
    good: "Example of correct usage"
    bad: "Example of incorrect usage"
```

### Creation Workflow

**Step 1: Draft Rule**
Prepare rule in YAML format following template above.

**Step 2: Safety Checks**
```markdown
□ Does this conflict with CLAUDE.md? (If yes → STOP)
□ Does this conflict with existing rules? (If yes → MERGE)
□ Is this specific and actionable? (If no → REFINE)
□ Is the impact measurable? (If no → ADD METRICS)
```

**Step 3: User Confirmation**
```markdown
I've identified a repeatable pattern worth codifying:

[Rule YAML]

Apply this rule to `.claude/rules/dynamic_rules.md`?
Reply: "yes" to apply, "modify" to change, "no" to cancel.
```

**Step 4: Implementation**
AFTER user confirmation:
1. Read existing `.claude/rules/dynamic_rules.md`
2. Append new rule (maintain YAML format)
3. Do NOT modify other rules
4. Confirm completion

**Step 5: Global Applicability Assessment (CRITICAL)**

在提议新规则时，必须评估其全局适用性和综合收益：

```markdown
### 全局适用性评估
- 适用范围: [所有对话/特定场景]
- 跨场景价值: [高/中/低]

### 综合收益评估
- token_saving: [X%] ✓/✗
- time_saving: [X%] ✓/✗
- error_prevention: [level] ✓/✗
- user_satisfaction: [level] ✓/✗
- performance: [level] ✓/✗

### 加入CLAUDE.md建议
- ✅ 值得加入（全局适用 + 综合收益好）
- ❌ 不建议加入（仅特定场景或收益不足）

[如果是✅，询问用户是否同时加入CLAUDE.md]
```

**加入CLAUDE.md的门槛**（用户明确要求）:
- ✅ 全局适用 + 综合收益好 → 加入CLAUDE.md
- ❌ 只适用于特定场景 → 仅保留在dynamic_rules.md

**示例**:
```
DR-017评估结果：
- 全局适用性: ✅ 适用于所有对话类型
- 综合收益: time_saving=66% ✓, performance=critical ✓
- 结论: ✅ 值得加入CLAUDE.md
```

### Prohibited Actions

🚫 **NEVER**:
- Modify `CLAUDE.md`
- Modify `.claude/skills/dialogue-optimizer/SKILL.md` (this file)
- Delete existing rules (use status: deprecated instead)
- Modify rule format (must use YAML template)
- Create rules without user confirmation

## Layer 4: Rule Lifecycle Management

### Health Monitoring

Check rule health when `.claude/rules/dynamic_rules.md` has ≥ 15 rules:

**Metrics**:
```markdown
Current rules: [count]
Active rules: [count]
Deprecated rules: [count]
Avg. token saving: [average%]
```

**Decision Tree**:
```
If total_rules ≥ 20:
  → Execute merge protocol

If deprecated_rules ≥ 5:
  → Execute archive protocol
```

### Merge Protocol

1. **Identify Similar Rules** - Consolidate redundant rules
2. **Update Merged Rules** - Set status: deprecated
3. **Confirm with User** - Get approval before merging

### Archive Protocol

1. **Move Deprecated Rules** - Copy to `.claude/rules/archived_rules.md`
2. **Maintain History** - Add archive_date and archive_reason
3. **Remove from Active** - Clean up dynamic_rules.md

---

## Layer 5-6: 扩展评估协议（按需加载）

### 评估能力概览

dialogue-optimizer V5.0提供三个扩展评估协议：

- **Layer 5**: Agent评估与优化协议
  - 触发检测（Agent是否按预期自动触发）
  - 输出质量评估（场景理解、务实性、语言特性）
  - **Token消耗评估**（输入/输出/性价比计算）
  - 错误模式识别（模板驱动、过度设计、教条主义）
  - 自动更新Agent功能

- **Layer 6**: Skill评估与优化协议
  - 触发与调用检测（调用方式、Skill vs Agent判断）
  - 功能完整性评估（核心功能、边界处理、文档质量）
  - **Token消耗评估**（性价比对比、优化建议）
  - 输出质量评估（准确性、完整性、可执行性）
  - 自动更新Skill功能

- **Layer 7**: 系统整体健康评估协议（新增）
  - **系统Token消耗总览**（Agent/Skill平均消耗、性价比对比）
  - Agent/Skill/Trigger/规则/协作五维度评估
  - 自测试用例（验证评估准确性）
  - **Token趋势分析**（持续改进追踪）

### 使用方式

```bash
# 评估Agent
用户：评估Code-Reviewer Agent
自动触发：Read layer5-agent-assessment.md → 执行Layer 5协议
输出：性能评分 + Token消耗 + 性价比 + 优化建议

# 评估Skill
用户：评估brainstorming skill
自动触发：Read layer6-skill-assessment.md → 执行Layer 6协议
输出：综合评分 + Token消耗 + 性价比 + 优化建议

# 系统健康评估
用户：评估整个系统 / 系统健康评估
自动触发：Read layer7-system-health.md → 执行Layer 7协议
输出：五维度评分 + Token总览 + 优化优先级 + 趋势分析

# 自我评估
用户：评估dialogue-optimizer skill
自动触发：Read layer6-skill-assessment.md → 执行Layer 6协议
输出：自我评分 + Token消耗 + 性价比
```

### 按需加载文件

```yaml
评估Agent时加载:
  文件: layer5-agent-assessment.md
  内容:
    - Agent性能评估（触发检测、输出质量、错误识别）
    - Agent优化建议（版本迭代、自动更新）
    - Agent评估报告模板
    - 自动化规则建议
    - 评估后自动行动流程

评估Skill时加载:
  文件: layer6-skill-assessment.md
  内容:
    - Skill性能评估（触发检测、功能完整性、输出质量）
    - Skill优化建议（功能缺失、文档改进、调用优化）
    - Skill评估报告模板
    - Skill生态系统评估
    - 常见Skill问题诊断
```

### 触发条件

**Layer 5自动触发**（满足任一）：
1. 对话中使用了任何Agent
2. 用户说"评估agent"、"分析agent"
3. 检测到Agent触发失败或输出质量问题

**Layer 6自动触发**（满足任一）：
1. 对话中使用了任何Skill
2. 用户说"评估skill"、"分析skill"
3. 检测到Skill输出质量问题

**Layer 7自动触发**（满足任一）：
1. 用户说"系统健康评估"、"整体评估"、"全系统检查"
2. 每月定期评估（建议每月1次）
3. 系统重大更新后（Agent/Skill/规则大版本更新）
4. 用户明确要求"评估整个系统"

### 文档拆分原因

```yaml
拆分前（V4.0）:
  文件大小: 974行
  加载时间: 每次调用skill都加载完整文件
  Token消耗: 约15K tokens

拆分后（V5.0）:
  核心文件: 369行（Layer 1-4）
  Agent评估: 按需加载layer5-agent-assessment.md
  Skill评估: 按需加载layer6-skill-assessment.md
  系统评估: 按需加载layer7-system-health.md
  Token节省: 评估Agent时节省约50%
  新增能力: Token消耗与性价比评估
```

### 完整文档路径

```
.claude/skills/dialogue-optimizer/
├── SKILL.md (核心: Layer 1-4, 369行)
├── layer5-agent-assessment.md (Agent评估协议 + Token评估)
├── layer6-skill-assessment.md (Skill评估协议 + Token评估)
├── layer7-system-health.md (系统健康评估 + 自测试)
└── archive/
    └── dialogue-optimizer-v3.2.md (历史版本)
```

---

## Optional Reading (按需加载)

如需深入了解设计原理，可读取：
- `.claude/skills/dialogue-optimizer/references/first-principles-summary.md` - 核心设计理念
- `.claude/skills/dialogue-optimizer/references/evolution-mechanism.md` - 进化机制详解

历史版本归档在 `archive/dialogue-optimizer-v3.2.md`

---

**Version**: Runtime V5.0 Full-Ecosystem (全生态评估版)
**Last Updated**: 2026-01-23
**Auto-Trigger**: Every conversation end + Agent/Skill usage detected
**New Features**:
- Agent性能评估（Layer 5）+ Token消耗评估
- Skill评估（Layer 6）+ Token消耗评估
- 系统整体健康评估（Layer 7）+ Token趋势分析
- 自测试用例（验证评估准确性）
