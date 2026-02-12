# Planning Mode Rules (Trigger 8)

> **Auto-Load Trigger**: Loaded when user requests planning or AI detects complex tasks.
> **Skill Source**: [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) v2.15.0 (Manus-style)

## 1. Trigger Conditions

**Explicit Request**:
- User says: "start planning", "make a plan", "planning mode", "enter plan mode"
- Slash command: `/planning-with-files` or `/plan`

**Complex Task Signals**:
- Keywords: "complex task", "multi-step", "research project", "analyze and optimize"
- AI heuristics: > 5 expected tool calls, multiple files/modules involved

**Project Start Signals**:
- User says: "new project", "refactor XXX", "design XXX architecture"
- AI heuristics: Requires multi-stage execution

**Exclusions**:
- Simple Q&A, single file edits, quick queries, code reviews

## 2. Automatic Execution Sequence

```bash
1. Detect Task Complexity
   └─ Keyword matching / Tool call estimation / Cross-file check

2. Check for Previous Session (Session Recovery v2.2.0+)
   └─ Run session-catchup.py to recover unsynced context after /clear
   └─ Check git diff --stat for actual code changes

3. Check Planning Files
   └─ ls task_plan.md findings.md progress.md

4. Create or Load Planning Files
   └─ Missing? → Execute .claude/skills/planning-with-files/scripts/init-session.ps1
   └─ Exists?  → Read and restore context

5. Enable Planning Rules
   └─ 2-Action Rule: Save to findings.md every 2 view/search ops
   └─ Pre-Decision Read: Read task_plan.md before major decisions
   └─ Error Logging: Log errors to task_plan.md
   └─ Completion Verify: Check task_plan.md before stopping

6. Guide User
   └─ Show status, confirm objectives, start execution
```

## 3. Planning File Structure (3-File Pattern)

| File | Purpose | When to Update |
|------|---------|----------------|
| `task_plan.md` | Phases, progress, decisions | After each phase |
| `findings.md` | Research, discoveries | After ANY discovery |
| `progress.md` | Session log, test results | Throughout session |

## 4. Core Principles (Manus Philosophy)

> **Context Window = RAM** (Volatile, Limited)
> **Filesystem = Disk** (Persistent, Infinite)
> → **Write all important info to disk**

| Principle | Implementation |
|-----------|----------------|
| Filesystem as memory | Store in files, not context |
| Attention manipulation | Re-read plan before decisions (hooks) |
| Error persistence | Log failures in plan file |
| Goal tracking | Checkboxes show progress |
| Completion verification | Stop hook checks all phases |

## 5. Key Rules

1. **Plan First**: Complex tasks MUST have `task_plan.md`. Non-negotiable.
2. **2-Action Rule**: Save findings every 2 view/browser/search operations.
3. **Pre-Decision Read**: Read `task_plan.md` before major decisions.
4. **Log ALL Errors**: Record failures to avoid repetition.
5. **Never Repeat Failures**: Track attempts, mutate approach.
6. **Verify Completion**: Check completion status before stopping.

## 6. The 3-Strike Error Protocol

```
ATTEMPT 1: Diagnose & Fix
  → Read error carefully, identify root cause, apply targeted fix

ATTEMPT 2: Alternative Approach
  → Same error? Try different method/tool/library
  → NEVER repeat exact same failing action

ATTEMPT 3: Broader Rethink
  → Question assumptions, search for solutions, update plan

AFTER 3 FAILURES: Escalate to User
  → Explain what you tried, share specific error, ask for guidance
```

## 7. The 5-Question Reboot Test

If you can answer these, your context management is solid:

| Question | Answer Source |
|----------|---------------|
| Where am I? | Current phase in task_plan.md |
| Where am I going? | Remaining phases |
| What's the goal? | Goal statement in plan |
| What have I learned? | findings.md |
| What have I done? | progress.md |

## 8. Usage Examples

**Auto-Trigger**:
User: "Optimize DashGo training flow"
AI: Detects complexity → Creates planning files → Enables planning mode

**Explicit Request**:
User: "Start planning this refactor"
AI: Triggers planning mode → Creates files → Guides phase definition

**Research Project**:
User: "Research notebooklm-skill implementation"
AI: Detects research → Enables planning mode → Uses findings.md for notes

## 9. Integration Details

- **Skill Location**: `.claude/skills/planning-with-files/`
- **Scripts (Windows)**: `scripts/init-session.ps1`, `scripts/check-complete.ps1`
- **Templates**: `templates/task_plan.md`, `templates/findings.md`, `templates/progress.md`

**Notes**:
- Files created in current working directory (project root).
- Context restoration supported via session-catchup.py.
- Auto-check completion on stop.
