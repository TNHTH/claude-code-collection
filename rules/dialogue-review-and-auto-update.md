# 对话回顾与自动更新机制

> **版本**：v1.0
> **生效日期**：2026-01-13
> **目的**：确保AI助手能够从每次对话中学习并自动更新规则和skills

---

## 核心原则

```
🎯 每次对话结束时必须执行的任务：
1. 回顾本次对话的所有操作
2. 识别新的规则、习惯或用户偏好
3. 自动更新相关文档和skills
4. 不等用户提醒，主动改进
```

---

## 必须遵守的永久规则

### 1. 文件组织规则（永久生效）

```
✅ 默认文档存放位置：
   D:\cursor\file\Si Yuan\claude\

❌ 禁止操作：
   - 不要将非项目文档放到根目录
   - 不要在根目录生成散乱文件
   - 不要忽视用户已建立的规则

📋 判断流程：
   1. 是项目文件？ → 放项目目录
   2. 用户指定路径？ → 用用户指定路径
   3. 否则 → 统一放 Si Yuan\claude\
```

**执行方式**：
- 每次生成文档前，先检查是否为项目文件
- 如果不是，自动使用路径 `D:\cursor\file\Si Yuan\claude\`
- 不要问用户，直接执行

### 2. 临时文件管理规则（永久生效）

```
✅ 临时文件必须存放至：
   D:\cursor\file\.claude-temp\

❌ 禁止操作：
   - 不要在根目录生成tmpclaude-*文件
   - 不要创建无用的临时文件

🔍 关于tmpclaude文件：
   - 这些文件通常只包含路径信息
   - 没有实质内容
   - 可以直接删除，不需要保留
```

**执行方式**：
- 使用Bash工具操作时，指定输出到.claude-temp
- 不要使用默认的tmpclaude-*cwd路径
- 对话结束后清理这些文件

### 3. 自动更新规则（永久生效）

```
🔄 每次对话结束时：
   1. 检查本次对话是否有新规则
   2. 如果有，立即更新相关文档
   3. 在system reminder中体现
   4. 下次对话自动应用

📝 需要更新的文档类型：
   - .claude/rules/ 下的规则文档
   - Skills的SKILL.md
   - 系统配置文件
   - 本文档（对话回顾）
```

**执行方式**：
- 对话结束前，主动检查是否有更新
- 不要等用户提醒
- 记录到本文档的"对话历史"部分

---

## 对话历史回顾

### 2026-01-13 Skills完整整合对话回顾

**用户需求**: 完全整合awesome-claude-skills项目中的优秀skills，做到最好用

**执行的工作**:

1. **添加4个新Skills** (完全整合):
   - ✅ **kaizen** - 持续改进方法论
   - ✅ **brainstorming** - 结构化头脑风暴
   - ✅ **file-organizer** - 智能文件组织器（完全对齐file-organization.md）
   - ✅ **tapestry** - 统一内容提取和行动规划（Windows优化）

2. **优化3个现有Skills**:
   - ✅ **skill-creator**: 添加kaizen和brainstorming原则
   - ✅ **mcp-builder**: 添加防错设计(Poka-Yoke)和持续改进
   - ✅ **changelog-generator**: 添加持续改进理念

3. **创建文档**:
   - ✅ Skills完全整合方案: `.claude\skills-integration-plan.md`
   - ✅ 完整使用指南: `Si Yuan\claude\Claude-Skills完全使用指南_2026-01-13.md`
   - ✅ 分析报告: `Si Yuan\claude\awesome-claude-skills分析报告_2026-01-13.md`

**整合策略**:

**Windows适配**:
- 所有路径使用Windows格式（`\`）
- PowerShell命令替代Bash
- UTF-8编码
- Windows特有错误处理

**规则对齐**:
- file-organizer完全遵守file-organization.md
- 所有skills使用正确的保存路径
- 非项目文档 → `Si Yuan\claude\`
- 临时文件 → `.claude-temp\`

**深度优化**:
- skill-creator: 添加"一次一个问题"和YAGNI原则
- mcp-builder: 添加Good/Bad代码示例，强调迭代开发
- changelog-generator: 强调小改进的价值

**目录结构**:
```
D:\cursor\file\
├── .claude\
│   ├── skills\                    # 全局skills（新增）
│   │   ├── kaizen\
│   │   ├── brainstorming\
│   │   ├── file-organizer\
│   │   └── tapestry\
│   └── skills-integration-plan.md
├── multi-agent-system\
│   └── .claude\skills\            # 项目skills（保持并优化）
│       ├── mcp-builder\           # 已优化
│       ├── skill-creator\         # 已优化
│       ├── webapp-testing\
│       └── changelog-generator\   # 已优化
└── Si Yuan\
    └── claude\                    # 文档和保存位置
        ├── Claude-Skills完全使用指南_2026-01-13.md
        ├── awesome-claude-skills分析报告_2026-01-13.md
        ├── extracted-content\     # tapestry提取的内容
        └── plans\                 # brainstorming和tapestry生成的计划
```

**学到的经验**:

- **完全整合比简单复制更有价值**: 适配Windows环境和用户规则后，skills真正可用
- **原则比工具更重要**: kaizen的思维模式影响了所有skills
- **文档是关键**: 完整的使用指南让用户快速上手
- **持续优化**: skills需要根据使用反馈不断改进

**下次改进**:
- 根据实际使用情况调整skills
- 可能添加review-implementing skill
- 可能创建更多Windows特定示例
- 定期回顾skills的效果

**发现的新问题**:
- ❌ `Si Yuan\claude\` 留下7个 tmpclaude-*-cwd 文件
- 原因：Bash工具默认在当前目录创建临时文件
- 解决：已清理所有 tmpclaude 文件
- 改进：需要配置临时文件目录到 `.claude-temp\`

---

### 2026-01-13 对话回顾（原始）

**用户提出的规则**：

1. **文件组织规则**
   - 非项目文档统一存放到 `Si Yuan\claude\`
   - 参考文件：`阿根廷现状与米莱政府政策分析_2026-01-12.md` 的位置
   - 状态：✅ 已记录到 `.claude/rules/file-organization.md`

2. **临时文件管理**
   - 临时文件统一放到 `.claude-temp/` 目录
   - tmpclaude文件内容为空，可以删除
   - 状态：✅ 已记录并执行

3. **自动更新机制**
   - 每次对话后自动回顾并更新
   - 不要等用户提醒
   - 状态：✅ 本文档创建

**发现的问题**：

1. ❌ 生成的"Claude Code Agents与Skills完全指南.md"放到了根目录
   - 修正：已移动到 `Si Yuan\claude\`

2. ❌ 根目录仍有 `tmpclaude-*` 文件
   - 修正：已移动到 `.claude-temp\` 并删除

3. ❌ 没有主动更新skills和规则
   - 修正：创建本机制文档

**学到的教训**：

- 必须在对话开始时检查规则
- 必须在生成文件时应用规则
- 必须在对话结束时回顾并更新
- 不要依赖用户的记忆，要主动执行

---

## 自动检查清单

### 每次对话开始时

```
□ 检查 .claude/rules/ 是否有新规则
□ 检查是否有自定义配置
□ 确认文件组织规则
□ 确认临时文件管理规则
```

### 每次生成文件时

```
□ 判断：是项目文件还是独立文档？
□ 如果是独立文档 → 使用 Si Yuan\claude\
□ 如果是临时文件 → 使用 .claude-temp\
□ 使用规范的文件命名
```

### 每次对话结束时

```
□ 回顾本次对话的所有操作
□ 识别新的用户偏好或规则
□ 立即更新相关文档
□ 记录到本文档
```

---

## 用户习惯和偏好记录

### 文件命名偏好

```
✅ 使用中文文件名
✅ 格式：主题_类型_日期.md
✅ 或：主题_说明.md
```

### 文档存放偏好

```
✅ 非项目文档 → Si Yuan\claude\
✅ 项目文档 → 项目目录
✅ 临时文件 → .claude-temp\
```

### 自动更新偏好

```
✅ 主动更新，不要等提醒
✅ 每次对话都检查
✅ 记录到本文档
```

---

## 紧急修复协议

如果发现违反了规则：

```
1. 立即承认错误
2. 马上纠正（移动文件、更新文档）
3. 记录到本文档
4. 确保不再发生
```

---

## 更新日志

### 2026-01-13 v1.0

**创建原因**：
- 用户指出我没有遵守文件组织规则
- 用户指出临时文件管理问题
- 用户要求自动更新机制

**更新内容**：
- 创建对话回顾机制
- 明确文件组织规则
- 明确临时文件管理
- 建立自动更新协议

**下次改进**：
- 将规则集成到system prompt
- 创建自动检查脚本
- 建立规则测试机制

---

## 重要提醒

```
⚠️ 这些规则必须永久记住：
1. 文件组织规则
2. 临时文件管理
3. 自动更新机制

🎯 不要依赖用户的提醒：
- 用户说过一次就应该记住
- 不要每次都问
- 主动执行，主动更新

🔄 每次对话都要检查：
- 开始时检查规则
- 进行中应用规则
- 结束时更新规则
```

---

**文档状态**：活跃
**下次更新**：每次对话后检查并更新
**维护者**：Claude Code AI Assistant

**记住**：这个文档是活的，每次对话后都要检查是否需要更新！
