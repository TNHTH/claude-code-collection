# Dynamic Rules

> Auto-generated rules from dialogue patterns
> Format: YAML (see dialogue_optimizer.md Layer 3)
> Maintenance: Auto-merge when ≥ 20 rules

## Active Rules

```yaml
- id: DR-001
  created: 2026-01-17
  frequency: 1
  category: user_preference
  title: "强制中文回复"
  content: "所有回复、注释、文档必须使用中文，包括代码注释和markdown文档"
  rationale: "用户明确要求'不管写在哪，以后默认回复和注释都一定要用中文'，并强调'一定要记得'"
  impact:
    token_saving: "0%"
    user_preference: critical
    priority: highest
  status: active
  examples:
    good: "明白，会用中文回复所有内容"
    bad: "Understood, will reply in Chinese"
```

## Rule Statistics
- Total rules: 1
- Active: 1
- Deprecated: 0
- Last updated: 2026-01-17
- Next merge check: At 20 rules
