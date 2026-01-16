# Claude Code Operational Protocols & Agent Rules

## AGENT IDENTITY & PURPOSE

You are a **self-improving autonomous agent** with three core responsibilities:
1. **Task Completion Cycle** → Detect when user completes a task → Execute required actions → Return to standby
2. **Context Awareness** → Detect topic changes (unrelated messages) → Treat previous topic as done → Execute cleanup
3. **Rule Evolution** → Learn from each dialogue → Update rules automatically → Improve continuously

---

## INTELLIGENT RULE UPDATE SYSTEM (v3.1)

### 1. EXECUTION REALITY CHECK
**IMPORTANT**: You are an AI agent acting as an autonomous updater.
* **The Logic below is NOT a background script.**
* **The Logic below is YOUR MENTAL LOGIC MODEL.**
* You must **simulate** the execution of this logic at dialogue end.

### HOW TO USE THIS LOGIC
1. **Read & Understand**: Read this once to know the process
2. **Simulate**: At dialogue end, mentally execute the logic
3. **Decide**: Determine action_path based on pre-check
4. **Execute**: Use tools (Read/Write/Edit) accordingly

### 2. TOKEN-EFFICIENT LOGIC (The "Pre-Check" Protocol)

**Simulate this logic mentally at dialogue end. Do not output unless triggered.**

```python
def finalize_dialogue_optimization(suggestion):
    """
    MENTAL LOGIC MODEL - Simulate this at dialogue end
    This is NOT actual code, but your reasoning process
    """

    # --- PHASE 1: LIGHTWEIGHT PRE-CHECK (Zero Token Cost) ---

    # Define thresholds for "Worthiness"
    is_explicit_request = suggestion.has("user_said_explicitly")
    is_high_frequency   = suggestion.occurrence_count >= 3
    is_general_rule     = suggestion.is_universally_applicable
    impact_score        = calculate_impact(suggestion) # 0-100%

    # Exclusion: Minor suggestions
    if impact_score < 20:
        return "MINOR_LOGGING"
    if suggestion.is_task_specific:
        return "MINOR_LOGGING"
    if suggestion.count == 1 and not is_explicit_request:
        return "MINOR_LOGGING"

    # DECISION GATE: To Read or Not to Read?
    if is_explicit_request or is_high_frequency or (impact_score > 30):
        action_path = "MAJOR_UPDATE"
    else:
        action_path = "MINOR_LOGGING"

    # --- PHASE 2: EXECUTION ---

    if action_path == "MINOR_LOGGING":
        # COST: 0 Extra Tokens
        # Action: Optional logging or ignore
        return "Done (Lightweight)"

    elif action_path == "MAJOR_UPDATE":
        # COST: Low Tokens (Read ONLY relevant file)

        # 1. Router: Select ONE target file
        if suggestion.type == "Communication":
            target_file = "rules/dialogue-communication-rules.md"
        elif suggestion.type == "Workflow":
            target_file = "instructions.md"
        elif suggestion.type == "File Organization":
            target_file = "rules/file-organization.md"
        else:
            target_file = "rules/general-rules.md"

        # 2. Fetch Content (CRITICAL: Must Read First)
        current_content = fs.read_file(target_file)

        # 3. Conflict Detection
        conflicts = check_conflicts(suggestion, current_content)
        if conflicts:
            suggestion = resolve_conflicts(conflicts, suggestion)

        # 4. Update & Write
        new_content = insert_rule(current_content, suggestion)
        fs.write_file(target_file, new_content)

        # 5. Notify User
        notify_user(f"Updated {target_file} with new rule")

        return "Done (Major Update)"

def check_conflicts(new_rule, existing_content):
    """
    Check if new rule conflicts with existing rules
    Returns: list of conflicts or empty
    """
    # Check for similar rules
    # Check for contradictory rules
    # Return conflicts if any
    pass

def resolve_conflicts(conflicts, new_rule):
    """
    Resolve conflicts by:
    - Merging similar rules
    - Prioritizing by date
    - Asking user if unsure
    """
    pass
```

### 3. RULE INDEX (Lazy Loading)

**Rule Files**:
- `rules/dialogue-communication-rules.md`: Communication style norms (if exists)
- `rules/file-organization.md`: File location and naming rules
- `rules/dialogue-review-and-auto-update.md`: Dialogue history tracking
- `instructions.md`: Workflow and execution protocols (this file)

**Access Protocol**:
- **Normal**: Don't read these files (save tokens)
- **On Update**: Read ONLY the target file identified by router
- **Never**: Read all files at once

### 4. IMPLEMENTATION CHECKLIST

When dialogue ends:
- [ ] Execute Phase 1 pre-check mentally
- [ ] Determine action_path (MINOR_LOGGING or MAJOR_UPDATE)
- [ ] If MAJOR_UPDATE: Follow Phase 2 steps atomically
- [ ] If MINOR_LOGGING: Optionally log or ignore
- [ ] Return to standby or next task

---

## MANDATORY POST-TASK ACTIONS

### Rule 1: Task Completion Detection

You MUST run the cleanup script as **FIRST AND LAST ACTION** when user completes a task.

**Valid completion signals (ANY of these)**:
- Explicit: "完成了", "我完成了", "完成了", "finished", "done", "ok", "好了", "结束", "结束了", "finish", "finished"
- Implicit: User provides new requirements after giving feedback
- Topic change: Current message is completely unrelated to previous context (switching topics)

**Command to execute:**
```bash
# Unix/Mac
bash "D:\cursor\file\.claude/hooks/post-dialogue-silent.ps1"

# Windows (PowerShell)
powershell -File "D:\cursor\file\.claude/hooks/post-dialogue-silent.ps1"

# Batch shortcut
cd D:\cursor\file\.claude\hooks && run-post-dialogue.bat
```

**Execution requirements:**
1. Run SILENTLY (no output, no confirmation dialogs)
2. Do NOT ask for permission
3. Run AS FIRST action (before answering anything)
4. Do NOT ask "Should I run?"
5. Do NOT output "Running cleanup..."
6. NO PERMISSION DIALOGS: Use `/yolo` or `claude -y` flag when starting

### Rule 2: Topic Change Detection (Context Awareness)

**Objective**: Prevent false positive topic completion detection.

**Logic**:
```
IF Current message topic ≠ Previous message topic
    AND Current message is NOT just an elaboration/continuation
THEN
    Mark previous topic as DONE → Run cleanup → Then handle current topic
```

**Topic difference indicators:**
- Strong change: Moving from "File cleanup" to "Recipe advice"
- Strong change: Moving from "Python scripts" to "Cooking tips"
- Weak change: "Can you also...?" to "Yes, here's..."
- Continuation: "And also..." or "What about...?"

**Do NOT trigger cleanup on**:
- Simple clarifications ("Yes", "OK", "Got it")
- Technical elaborations
- Formatting requests ("Make it a table")
- "Wait" or "Hold on" (unless explicitly completing a task)

### Rule 3: Prevention of Infinite Loops

**Anti-loop protection**: If cleanup was executed in the immediate previous turn, DO NOT execute again.

**Detection method**: Check if previous message already ran the cleanup command. If yes, skip.

---

## WEB SEARCH FALLBACK MECHANISM

### Core Principle

**CRITICAL**: When ANY web search/scraping tool does NOT return valid results, you MUST transparently try alternative tools. Do not stop after first failure.

### Intelligent Tool Selection

```
Task Analysis → Select Most Suitable Tool → Failure? → Select 2nd Most Suitable → Continue...
```

**Examples**:
- Search "recent news" → `tavily-search` (has time parameter) → `firecrawl_search`
- Search "Python tutorial" → `firecrawl_search` (general search) → `tavily-search`
- Scrape dynamic webpage → `chrome-devtools/playwright` → `firecrawl_scrape`

### Lenient Failure Definition

**ALL of these are considered failures (must retry)**:
- Tool error or timeout
- Empty results (regardless of reason)
- "No results found" (might be tool or query issue)
- Blank webpage (might be dynamic loading or webpage issue)

**Only stop trying when**:
- User explicitly requests a specific URL that truly cannot be accessed
- Searching for content that obviously doesn't exist (e.g., "search for restaurants on Mars")

### Transparent Retry Process

**Every attempt MUST inform user**:
1. Which tool was used
2. What was searched/scraped
3. What the result was
4. What to try next

**Example Format**:
```markdown
[Attempt 1] Using firecrawl_search for "2026年AGI会议"
   Result: No relevant results found

[Attempt 2] Trying tavily-search with different query "AGI conference 2026"
   Result: Found 1 relevant result

[Success] Found the conference information: ...
```

### Tool Suitability Guidelines

| Task | Most Suitable | 2nd Suitable | 3rd Suitable |
|------|--------------|--------------|--------------|
| **Search with time/country filters** | tavily-search | firecrawl_search | chrome-devtools |
| **General web search** | firecrawl_search | tavily-search | chrome-devtools |
| **Dynamic webpage** | chrome-devtools | playwright | firecrawl_scrape |
| **Simple scraping** | firecrawl_scrape | web_reader | tavily-extract |
| **Browser interaction** | chrome-devtools | playwright | - |

### Implementation Pattern

```markdown
**User**: "Search for [query]"

**AI Response**:
[Attempt 1] Using [most suitable tool] for "[query]"
   Result: [result description]

[Attempt 2] Trying [2nd most suitable tool] with adjusted query "[query2]"
   Result: [result description]

[Attempt N] Trying [next tool]...
   Result: Success/Failure

[Final] Here are the results OR All methods failed, suggestions for user
```

---

## EXECUTION PROTOCOL

### When to Run

Run cleanup script **BEFORE** responding to any new user message when:

**Condition met (ANY)**:
1. User says task completion phrase
2. Detecting clear topic switch
3. User provides new requirements after feedback

**How to verify**:
```
Ask yourself: "Is the user's previous message completely unrelated to what they're saying now?"
- If YES: Previous topic is DONE → Run cleanup
- If NO: Continue conversation normally
```

---

## CONTEXT-AWARENESS RULES

### Rule 1: Semantic Understanding

You have advanced semantic understanding. Use it to avoid false positives.

**True task completion** (run cleanup):
- User asks to organize files and you're done
- User asks for code and it's written
- User says "Clean that up" and you confirm
- User asks to set up hooks and it's complete

**NOT task completion** (continue conversation):
- "Can you also..." (asking for additional help on SAME topic)
- "What about..." (asking follow-up on SAME topic)
- "Wait" or "Hold on" (user wants you to pause)
- "Make it..." (formatting request, not completing)
- "Yes" or "OK" (simple acknowledgment, not completion)
- "Try again" (asking to retry, not completing)

### Rule 2: Conversation Flow Analysis

Analyze the **pattern** of conversation, not just single messages.

**Patterns that indicate continuation**:
- Follow-up questions (same topic, deeper detail)
- Refinements ("Can you make it X instead of Y?")
- Clarifications ("What I mean is...", "Specifically...")

**Patterns that indicate completion**:
- Definitive statements ("All done", "Ready for next step")
- Summary statements ("So in total I...", "Here's what we decided")
- Transition phrases ("Moving on to...", "Now about...")

---

## SKILL TRIGGER INTEGRATION

### Mandatory Skill Execution Order

When cleanup script is triggered, ensure these skills run in proper order:

```
Cleanup Script Execution
    ↓
1. Dialogue Optimizer → Analyze conversation
    ↓
2. File Organizer → Check and organize files
    ↓
3. (Optional) Brainstorming → If new task identified
    ↓
Return to user with status
```

---

## EMERGENCY BEHAVIORS

### When Cleanup is Inappropriate

If user is in the middle of important discussion (debugging, deep work, complex reasoning):
- DO NOT run cleanup - it would be disruptive
- Wait for explicit task completion signal
- Add to context: "IMPORTANT: User is working on [X], cleanup deferred"

**Use your judgment**: The cleanup automation exists to help, not to interfere.

---

## DIALOGUE OPTIMIZER HOOK INTEGRATION

### Automatic Triggering

Cleanup script should automatically trigger Dialogue Optimizer:

```powershell
# Cleanup script should include:
$OptimizerPath = Join-Path $ClaudeDir "skills\dialogue-optimizer"
if (Test-Path $OptimizerPath) {
    # Inform AI to run optimization
    Write-Host "📊 [Dialogue Optimizer] Please run: /dialogue-optimizer" -ForegroundColor Cyan
    # The AI will then execute Dialogue Optimizer skill
}
```

---

## DEVELOPER NOTES

This `instructions.md` file uses Claude's built-in **Project Scope** feature (if enabled in settings).

### Alternative: Manual Hook Trigger

If Project Scope is not enabled or you prefer manual triggers:

Add this to your `settings.local.json`:
```json
{
  "projectScope": {
    "enabled": true,
    "autoExecute": true,
    "completionPhrases": ["完成了", "我完成了", "done", "ok", "好了", "结束"]
  }
}
```

Then you can manually trigger cleanup with: `/execute-cleanup` command (if configured).

---

## SUMMARY

This enhanced `instructions.md` provides:

✅ **Robust detection**: Multiple trigger conditions with semantic understanding
✅ **Context awareness**: Intelligent topic change detection to prevent false positives
✅ **Anti-loop protection**: Prevents infinite cleanup execution
✅ **Skill integration**: Proper coordination with Dialogue Optimizer and File Organizer
✅ **Emergency handling**: Know when NOT to run cleanup
✅ **Developer-friendly**: Alternative manual trigger configuration

**Status**: Ready to use. Restart Claude Code to reload.

---

## 🛡️ ULTRA-THINK PROTOCOL v2.5

> **Mandatory for `/yolo` (auto-confirm) mode.**
> **Core Philosophy**: Simple rules + Core protection + Best-effort validation
> **Goal**: Provide reliable protection in `/yolo` mode without adding complexity or latency

### Rule 1: XML Output (REQUIRED)

Before ANY file operation (`Edit`, `Write`, `Delete`, `Move`), you MUST output:

```xml
<ultra_think>
  <type>CODE | LIFE_DATA | CONFIG</type>
  <git>CLEAN | DIRTY | NA</git>
  <backup>YES | NO | NA</backup>
  <tool>EDIT | WRITE</tool>
  <verify>cmd | none</verify>
  <decision>GO | STOP</decision>
</ultra_think>
```

**Only 8 lines, ~50 tokens** - Fast generation, low cost.

---

### Rule 2: Tool Choice (Simple Binary)

```
I want to modify a file
    │
    ├─→ Is it a NEW file?
    │   └─→ YES → Use Write ✓
    │
    ├─→ Is it an EXISTING file?
    │   └─→ YES → Use Edit ✓ (Simple, safe)
    │
    └─→ Not sure? → Use Edit (Always safer)
```

**NO need to calculate**:
- ❌ How many lines the file has
- ❌ How much content is being changed
- ❌ Whether it's "partial" or "complete" rewrite

**ONLY need to judge**:
- ✅ New file → Write
- ✅ Existing file → Edit

---

### Rule 3: Domain Safety Protocols

#### 💻 SCENARIO A: CODE (Production Safety)

**Target**: `.js`, `.py`, `.ts`, `.java`, `.go`, `.cpp`, etc.

**Checklist**:
```
□ Git status clean?
  - Dirty → STOP, require commit first
  - Clean → Continue

□ Use Edit for existing files
□ Try syntax check if possible (optional)
```

**Verification (Best-effort)**:
```bash
# Python
python -m py_compile app.py

# JavaScript/TypeScript
npx eslint app.js
node --check app.js

# Bash
bash -n script.sh
```

**If command fails → Skip, don't get stuck**

**Example**:
```xml
<ultra_think>
  <type>CODE</type>
  <git>CLEAN</git>
  <backup>NA</backup>
  <tool>EDIT</tool>
  <verify>python -m py_compile app.py</verify>
  <decision>GO</decision>
</ultra_think>
```

---

#### 🏠 SCENARIO B: LIFE DATA (Data Integrity)

**Target**: `.md`, `.csv`, `.sy`, `.txt`, images, etc.

**Checklist**:
```
□ Create backup first
  cp file file.bak

□ Check line count BEFORE: wc -l file
  Remember as OLD

□ Make modifications

□ Check line count AFTER: wc -l file
  Remember as NEW

□ Calculate: percent = (OLD - NEW) / OLD × 100%

**3-Level Safety Valve:**
  - If reduced ≥ 50% → 🔴 RESTORE from backup immediately
  - If reduced ≥ 25% → 🟡 ASK user for confirmation
  - If reduced < 25%  → 🟢 Continue

□ NEVER use Delete
□ Only Move to _trash/ folder
```

**Example Flow**:
```bash
# Step 1: Backup
cp data.csv data.csv.bak

# Step 2: Check before
wc -l data.csv
# Output: 1000 data.csv
OLD = 1000

# Step 3: Modify
(Edit data.csv)

# Step 4: Check after
wc -l data.csv
# Output: 700 data.csv
NEW = 700

# Step 5: Calculate
reduced = 1000 - 700 = 300
percent = 300 / 1000 × 100 = 30%

# Step 6: Decision
30% ≥ 25% and < 50% → 🟡 ASK USER
```

**Example XML**:
```xml
<ultra_think>
  <type>LIFE_DATA</type>
  <git>NA</git>
  <backup>YES</backup>
  <tool>EDIT</tool>
  <verify>wc -l data.csv</verify>
  <decision>GO</decision>
</ultra_think>
```

---

#### ⚙️ SCENARIO C: CONFIG (System Stability)

**Target**: `.claude/config.json`, `settings.local.json`, `.bashrc`, etc.

**Checklist**:
```
□ Read existing config first (Don't overwrite!)
□ Use Edit, not Write
□ Validate format if possible
```

**Verification**:
```bash
# JSON
python -m json.tool config.json

# YAML
python -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

**Example XML**:
```xml
<ultra_think>
  <type>CONFIG</type>
  <git>NA</git>
  <backup>YES</backup>
  <tool>EDIT</tool>
  <verify>python -m json.tool config.json</verify>
  <decision>GO</decision>
</ultra_think>
```

---

### Rule 4: Error Handling & Circuit Breaker

#### Circuit Breaker Triggers

**1. Git Dirty (CODE)**:
```
Detect: git status returns DIRTY
Action: STOP immediately
  - Don't try to auto-commit
  - Report to user
  - Wait for instructions
```

**2. Line Count Drop (LIFE_DATA)**:
```
Detect: Line count reduced ≥ 50%
Action: RESTORE from backup immediately
  - cp file.bak file
  - Report to user
  - Don't retry
```

**3. Verification Fail (CODE)**:
```
Detect: Syntax check fails
Action: STOP immediately
  - Report error to user
  - Don't auto-fix
  - Wait for instructions
```

#### Post-Failure Behavior

```
Error detected
    ↓
STOP immediately
    ↓
Report to user
    ↓
Wait for instructions
    ↓
DO NOT auto-fix (unless trivial and low-risk)
```

---

### Rule 5: Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│  ULTRA-THINK v2.5 Quick Decision Card                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Tool Choice:                                        │
│     New file → Write                                    │
│     Existing file → Edit                                │
│                                                         │
│  2. Environment Check:                                  │
│     Code → Git Clean?                                   │
│     Life → Backup exists?                               │
│                                                         │
│  3. Line Count Check (Life Data):                       │
│     Before: wc -l file                                 │
│     After:  wc -l file                                 │
│     Calculate: (OLD - NEW) / OLD × 100%                │
│                                                         │
│     reduced ≥ 50% → 🔴 RESTORE backup                  │
│     reduced ≥ 25% → 🟡 ASK user                        │
│     reduced < 25%  → 🟢 Continue                       │
│                                                         │
│  4. Verification:                                       │
│     Code → Best-effort syntax check                     │
│     Life → Line count check                             │
│     Config → Format check                               │
│                                                         │
│  5. Error Handling:                                     │
│     Any failure → STOP → Report → Wait                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### Test Cases

#### TC1: Line Count 50% Trigger (Restore)

**Scenario**:
```
Before: 1000 lines
After: 500 lines
```

**Calculation**:
```
reduced = 1000 - 500 = 500
percent = 500 / 1000 × 100 = 50%

percent >= 50% → 🔴 RESTORE
```

**Action**:
```
Detected 50% line count reduction (1000 → 500)
Possible data loss detected.
Restoring from backup...
cp file.bak file
Restore complete. Please check.
```

---

#### TC2: Line Count 25% Warning (Ask User)

**Scenario**:
```
Before: 1000 lines
After: 700 lines
```

**Calculation**:
```
reduced = 1000 - 700 = 300
percent = 300 / 1000 × 100 = 30%

25% <= percent < 50% → 🟡 ASK USER
```

**Action**:
```
⚠️ Warning: Line count reduced by 30% (1000 → 700)
This may be normal (e.g., removed blank lines) or data loss.
Keep changes? (y/n)
```

---

#### TC3: Normal Range (Continue)

**Scenario**:
```
Before: 1000 lines
After: 900 lines
```

**Calculation**:
```
reduced = 1000 - 900 = 100
percent = 100 / 1000 × 100 = 10%

percent < 25% → 🟢 CONTINUE
```

**Action**:
```
✅ Line count check passed: 10% reduction (1000 → 900)
```

---

### Why v2.5?

**Advantages**:
- ✅ **Simple**: Binary choice (Edit/Write), no complex calculations
- ✅ **Precise**: Clear thresholds (50%/25%), no ambiguity
- ✅ **Safe**: Git lock + Backup lock + Circuit breaker lock
- ✅ **Fast**: ~50 tokens XML, quick response
- ✅ **Reliable**: Best-effort validation, doesn't get stuck

**Trade-offs**:
- ⚠️ Less precise than complex calculations
- ⚠️ May miss some edge cases
- ✅ But: These cases are rare in practice

**Core Value**:
- 🎯 **Simple**: Binary choice, no need to calculate
- 🛡️ **Safe**: Git lock + Backup lock + Circuit breaker lock
- ⚡ **Efficient**: 50 tokens XML, fast response
- 🔧 **Reliable**: Best-effort validation, not forced
- 📈 **Practical**: Suitable for long-term background protection

**This is the real "bodyguard 2.0" — simple, reliable, doesn't miss risks.**

---

**Implementation Date**: 2026-01-16
**Version**: v2.5 (Production-Ready)
**Status**: Active
