# Planning Mode Rules (Trigger 8)

> **Auto-Load Trigger**: Loaded when user requests planning or AI detects complex tasks.

## 1. Trigger Conditions

**Explicit Request**:
- User says: "start planning", "make a plan", "planning mode", "enter plan mode"

**Complex Task Signals**:
- Keywords: "complex task", "multi-step", "research project", "analyze and optimize"
- AI heuristics: > 5 expected tool calls, multiple files/modules involved

**Project Start Signals**:
- User says: "new project", "refactor XXX", "design XXX architecture"
- AI heuristics: Requires multi-stage execution

**Exclusions**:
- Simple Q&A, single file edits, quick queries, code reviews (use Code-Reviewer Agent)

## 2. Automatic Execution Sequence

```bash
1. Detect Task Complexity
   └─ Keyword matching / Tool call estimation / Cross-file check

2. Check Planning Files
   └─ ls task_plan.md findings.md progress.md

3. Create or Load Planning Files
   └─ Missing? → Execute ~/.claude/plugins/planning-with-files/scripts/init-session.sh
   └─ Exists?  → Read and restore context

4. Enable Planning Rules
   └─ 2-Action Rule: Save to findings.md every 2 view/search ops
   └─ Pre-Decision Read: Read task_plan.md before major decisions
   └─ Error Logging: Log errors to task_plan.md
   └─ Completion Verify: Check task_plan.md before stopping

5. Guide User
   └─ Show status, confirm objectives, start execution
```

## 3. Planning File Structure

- **task_plan.md**: Phase breakdown, progress tracking, decision log
- **findings.md**: Research findings, technical decisions, known issues
- **progress.md**: Session logs, test results, error tracking

## 4. Core Principles

> **Context Window = RAM** (Volatile, Limited)
> **Filesystem = Disk** (Persistent, Infinite)
> → **Write all important info to disk**

## 5. Key Rules

1. **Plan First**: Complex tasks MUST have `task_plan.md`.
2. **2-Action Rule**: Save findings every 2 operations.
3. **Pre-Decision Read**: Read `task_plan.md` before major decisions.
4. **Log Errors**: Record failures to avoid repetition.
5. **Verify Completion**: Check completion status before stopping.

## 6. Usage Examples

**Auto-Trigger**:
User: "Optimize DashGo training flow"
AI: Detects complexity → Creates planning files → Enables planning mode

**Explicit Request**:
User: "Start planning this refactor"
AI: Triggers planning mode → Creates files → Guides phase definition

**Research Project**:
User: "Research notebooklm-skill implementation"
AI: Detects research → Enables planning mode → Uses findings.md for notes

## 7. Integration Details

- **Plugin**: `~/.claude/plugins/planning-with-files/`
- **Skill**: `.agent/skills/planning-with-files/SKILL.md`
- **Scripts**: `scripts/init-session.sh`, `scripts/check-complete.sh`

**Notes**:
- Files created in current working directory.
- Context restoration supported via file reading.
- Auto-check completion on stop.
