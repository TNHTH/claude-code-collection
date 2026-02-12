---
name: obsidian-gardener
description: |
  Obsidian知识库自动整理工具。触发词：整理收集箱、整理笔记、vault整理、归档文件、清理inbox、笔记管理、合并笔记、添加链接。
  Automates Obsidian vault organization by scanning, linking, merging, and maintaining notes.
version: 2.0
author: Claude
---

This skill provides advanced tools for the Obsidian Auto-Organizer System (Smart Gardener). It handles scanning, organizing, linking, merging, and enriching notes.

## Tools

### `scan_vault`
Scans the vault structure and rebuilds the `vault_index.json` map.
- **Usage**: `python .claude/skills/obsidian-gardener/scripts/indexer.py --vault-path "D:\cursor\file\Si Yuan" --output "D:\cursor\file\.claude\vault_index.json"`

### `read_inbox`
Reads files in the `00_收集箱` folder for processing.
- **Usage**: `python .claude/skills/obsidian-gardener/scripts/mover.py read_inbox --vault-root "D:\cursor\file\Si Yuan"`

### `move_and_enrich`
Moves a file and updates metadata (Frontmatter).
- **Params**: `source`, `dest-folder`, `frontmatter` (json string)
- **Usage**: `python .claude/skills/obsidian-gardener/scripts/mover.py move ...`

### `auto_link`
Scans a note and automatically adds [[wikilinks]] for keywords that match existing note titles in the vault.
- **Params**:
  - `file-path`: Relative path of the note to process
- **Usage**:
  ```bash
  python .claude/skills/obsidian-gardener/scripts/gardener.py auto_link --vault-root "D:\cursor\file\Si Yuan" --index-path "D:\cursor\file\.claude\vault_index.json" --file-path "00_收集箱/MyNote.md"
  ```

### `merge_notes`
Merges multiple notes into a single note. Useful for combining fragments.
- **Params**:
  - `files`: List of relative paths (space separated)
  - `output`: Output relative path
  - `delete-sources`: (Optional) Flag to delete original files
- **Usage**:
  ```bash
  python .claude/skills/obsidian-gardener/scripts/gardener.py merge --vault-root "D:\cursor\file\Si Yuan" --output "10_Projects/Merged.md" --files "00_收集箱/Part1.md" "00_收集箱/Part2.md"
  ```

### `append_content`
Appends text to an existing note.
- **Params**: `target`, `content`
- **Usage**: `python .claude/skills/obsidian-gardener/scripts/gardener.py append ...`

## Workflow & Safety Protocols

### 收集箱处理工作流

对 `00_收集箱` 中的每个文件执行：
1. **读取内容** → 分析主题和类别
2. **判断操作**：
   - 碎片笔记？→ 等待其他部分 或 合并到已有笔记
   - 完整文章？→ 自动互链 → 添加 frontmatter → 移动到目标目录
   - 已有笔记的更新？→ 追加内容到已有文件

### 安全协议（不可违反）

1. **永远不删除内容** — 必须先合并再删除源文件
2. **移动前验证目标路径存在** — 不存在则先创建
3. **优先链接而非复制** — 避免内容重复
4. **Frontmatter 必须在文件首行** — 严禁前置任何字符（参考 DR-027）

### Frontmatter 标准

```yaml
---
created: YYYY-MM-DD
tags: [topic1, topic2]
status: processed
---
```

### 目录映射

| 内容类型 | 目标目录 |
|:---|:---|
| 学习笔记 | `Si Yuan/学习笔记/` |
| 日记/周记 | `Si Yuan/日记/` 或 `Si Yuan/周记/` |
| 生活经验 | `Si Yuan/生活经验/` |
| 新闻时事 | `Si Yuan/世界变化/` |
| 待分类 | 保留在 `Si Yuan/00_收集箱/` |

## Configuration
- **Vault Root**: `D:\cursor\file\Si Yuan`
- **Index**: `.claude/vault_index.json`
