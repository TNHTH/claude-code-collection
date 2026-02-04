---
name: obsidian-gardener
description: Automates Obsidian vault organization by scanning structure, reading inboxes, and enriching files.
version: 1.0
author: Claude
---

This skill provides tools for the Obsidian Auto-Organizer System (Smart Gardener). It handles scanning the vault structure, reading the inbox, and safely moving/enriching files.

## Tools

### `scan_vault`
Scans the "Si Yuan" directory and rebuilds the `vault_index.json` map.

- **Parameters**:
  - `refresh` (boolean, optional): Whether to force a refresh (not strictly used by script yet but good for intent).
- **Usage**:
  ```bash
  python .claude/skills/obsidian-gardener/scripts/indexer.py --vault-path "D:\cursor\file\Si Yuan" --output "D:\cursor\file\.claude\vault_index.json"
  ```

### `read_inbox`
Reads all files in the `00_收集箱` folder, providing a content preview (head/tail) for classification.

- **Parameters**: None (defaults to configured paths)
- **Usage**:
  ```bash
  python .claude/skills/obsidian-gardener/scripts/mover.py read_inbox --vault-root "D:\cursor\file\Si Yuan"
  ```

### `move_and_enrich`
Moves a file from the inbox to a destination folder, updating its frontmatter.

- **Parameters**:
  - `source_path` (string): Absolute path to the source file.
  - `dest_folder` (string): Relative path to the destination folder (e.g., "10_项目/Active").
  - `frontmatter` (string): JSON string representing key-value pairs to add/update in frontmatter.
  - `dry_run` (boolean, optional): If true, simulates the move without changing files.
- **Usage**:
  ```bash
  python .claude/skills/obsidian-gardener/scripts/mover.py move --vault-root "D:\cursor\file\Si Yuan" --source "absolute/path/to/file.md" --dest-folder "Target/Folder" --frontmatter "{\"status\": \"processed\"}"
  ```

## Configuration
- **Vault Root**: `D:\cursor\file\Si Yuan`
- **Inbox**: `00_收集箱`
- **Index File**: `.claude/vault_index.json`

## Common Errors & Solutions
1. **Vault path not found**: The script cannot locate the Obsidian vault.
   - *Solution*: Verify the `vault_root` path in `.claude/config.json` is absolute and correct.
2. **Permission denied**: Cannot move or read files in the vault.
   - *Solution*: Ensure the file is not open in another program and you have write permissions.
3. **Encoding errors**: Text content contains unsupported characters.
   - *Solution*: Ensure all markdown files are UTF-8 encoded.

## Common Errors & Solutions
1. **Vault path not found**: The script cannot locate the Obsidian vault.
   - *Solution*: Verify the `vault_root` path in `.claude/config.json` is absolute and correct.
2. **Permission denied**: Cannot move or read files in the vault.
   - *Solution*: Ensure the file is not open in another program and you have write permissions.
3. **Encoding errors**: Text content contains unsupported characters.
   - *Solution*: Ensure all markdown files are UTF-8 encoded.
