# File Organization Rules

## Document Storage Rules

### Default Document Location

Unless the user **explicitly specifies a path** or the document belongs to a **specific project**, all generated documents should be stored in:

```
~/Documents/claude/
```

### Scope

✅ **Documents to store in `~/Documents/claude/`:**
- Popular science documents (e.g., investment strategies, technical concepts)
- Analysis reports (e.g., industry analysis, policy analysis)
- Learning notes
- Any independent documents not related to projects

❌ **Documents NOT to store in `~/Documents/claude/`:**
- Documents with user-specified paths
- Files belonging to specific projects
- Project code and configuration files

### File Naming Conventions

- Use Chinese filenames for easy identification
- Format: `Topic_Type_YYYY-MM-DD.md`
  - Example: `Low-Volatility_Investment_Strategy_2025-01-13.md`
  - Example: `Argentina_Status_Analysis_2026-01-12.md`
- Can omit date if not important: `Investment_Strategy_Guide.md`

### Examples

**Correct operation**:
```
User: Generate a document about xxx
AI: [Generate document to] ~/Documents/claude/xxx_Guide.md
```

**User-specified path**:
```
User: Generate a document to docs/tutorial.md
AI: [Generate document to] docs/tutorial.md (follow user-specified path)
```

---

## Temporary File Management Rules

### Temporary File Storage Location

All temporary files should be stored in:

```
~/.claude-temp/
```

### Temporary File Types

- `tmpclaude-*-cwd` - Claude temporary working directories
- Temporary test files
- Temporary script files
- Any files not needed long-term

### Cleanup Strategy

- Clean up `.claude-temp/` files after conversation ends
- Keep `.claude-temp/` folder itself
- Use cleanup scripts: `cleanup-claude-temp.sh` or `cleanup-claude-temp.bat`

### Notes

⚠️ **Do NOT** generate scattered temporary files in the root directory
⚠️ **Do NOT** commit temporary files to Git repository (already configured in `.gitignore`)

---

## Execution Checklist

### When generating new documents

```
□ Is it a project file?
  - Yes → Store in project directory
  - No → Continue check

□ Did user explicitly specify path?
  - Yes → Use user-specified path
  - No → Store in ~/Documents/claude/

□ Check if target directory exists
  - Does not exist → Create directory

□ Use standardized file naming
```

### When creating temporary files

```
□ Confirm if file is temporary
□ Store in .claude-temp/ directory
□ Remind user to clean up after conversation
```

---

## Automation Suggestions

### Recommended Configuration (optional)

Add auto-cleanup hooks in user configuration:
- At conversation start: Check and clean scattered temp files in root
- At conversation end: Prompt user whether to clean temp files

### Quick Commands

Create shell alias:
```bash
# Clean temporary files
alias cct='bash cleanup-claude-temp.sh'
```

---

**Rule version**: v1.0
**Effective date**: 2025-01-13
**Scope**: All AI assistant conversations
