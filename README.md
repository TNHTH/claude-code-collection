# Claude Code 配置合集（中文版）

> 完整的Claude Code配置集合：Agents、Skills、规则、最佳实践

---

## ✨ 特性

- **7个专业Agent**：Product（需求分析）、Architect（架构设计）、Backend（后端）、Frontend（前端）、Code-Reviewer（代码审查）、Docs（文档）、DevOps（部署）
- **5个高效Skills**：dialogue-optimizer V5.0（对话优化）、brainstorming（头脑风暴）、kaizen（持续改进）、file-organizer（文件管理）、tapestry（内容处理）
- **18条动态规则**：从对话历史中总结的最佳实践
- **Token消耗评估框架**：Agent/Skill性价比分析
- **系统健康评估协议**：五维度评估

---

## 📦 内容结构

```
├── .claude/                    # Claude配置
│   ├── instructions.md        # 核心指令
│   ├── rules/                 # 规则文件
│   │   ├── coding-style.md    # 编码规范
│   │   ├── dynamic_rules.md   # 动态规则
│   │   └── file-organization.md
│   └── skills/                # Skills
│       ├── dialogue-optimizer/
│       ├── brainstorming/
│       ├── kaizen/
│       ├── file-organizer/
│       └── tapestry/
├── multi-agent-system/        # Agent系统
│   └── agents/               # 7个专业Agent
└── CLAUDE.md                  # 项目主文件
```

---

## 🚀 快速开始

### 1. 复制到你的项目

```bash
# 克隆仓库
git clone https://github.com/TNHTH/claude-code-collection.git

# 复制.claude/到你的项目
cp -r claude-code-collection/.claude/ your-project/
```

### 2. 自定义配置

修改以下路径为你的本地路径：

**文件组织规则** (`.claude/rules/file-organization.md`):
```diff
- D:\cursor\file\Si Yuan\claude\
+ ~/Documents/claude/
```

**临时文件路径**:
```diff
- D:\cursor\file\.claude-temp\
+ {PROJECT_ROOT}/.claude-temp/
```

### 3. 核心功能

**智能开发Agent系统**（Trigger 1）:
- 用户说"新建项目" → 自动触发7-Agent流水线
- 用户说"代码审查" → 自动触发Code-Reviewer Agent
- 用户说"写需求" → 自动触发Product Agent

**对话优化Skill**（DR-014）:
- 用户说"评估" → 自动调用dialogue-optimizer进行Full Assessment

**文件管理Skill**:
- 自动识别项目文件 vs 文档文件
- 自动归类到正确目录

---

## 📊 动态规则 (DR-001 ~ DR-018)

核心规则：
- **DR-001**: 强制中文回复
- **DR-002**: 工具失败自动切换
- **DR-006**: 极端高效对话风格
- **DR-008**: Agent vs Skill区别
- **DR-015**: 创建Skill/Agent时同步添加触发器
- **DR-016**: 方案执行前必须等待用户确认
- **DR-017**: 多文件读取必须并行（节省66%时间）

---

## 🛠️ 技术栈

- **语言**: Python, JavaScript/TypeScript, Go
- **框架**: 通用（不依赖特定框架）
- **工具**: Git, GitHub, MCP

---

## 📝 文档

- [Claude Code官方文档](https://docs.anthropic.com/claude-code)
- [参考项目：everything-claude-code](https://github.com/affaan-m/everything-claude-code)

---

## ⚖️ License

MIT

---

## 🤝 Contributing

欢迎提交Issue和Pull Request！

---

## 📧 Contact

- GitHub: [@TNHTH](https://github.com/TNHTH)

---

**最后更新**: 2026-01-22
