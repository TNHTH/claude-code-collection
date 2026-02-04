import os
import shutil
import hashlib
import json
import re
import argparse
import time
from pathlib import Path
from datetime import datetime

# --- Helper Functions ---

def calculate_checksum(file_path):
    """Calculates SHA256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def read_head_tail(file_path, head_lines=50, tail_lines=20):
    """Reads the first N and last M lines of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if len(lines) <= (head_lines + tail_lines):
            return "".join(lines)

        head = lines[:head_lines]
        tail = lines[-tail_lines:]
        return "".join(head) + "\n...[truncated]...\n" + "".join(tail)
    except Exception as e:
        return f"Error reading file: {str(e)}"

def extract_frontmatter(content):
    """Extracts YAML frontmatter as a dictionary and returns the rest of the content."""
    # Regex to find YAML block at the start of the file
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if match:
        yaml_text = match.group(1)
        body = match.group(2)
        try:
            # Simple YAML parsing (avoids pyyaml dependency if possible for simple key-values)
            # For robustness, we'll try to use a simple dict comprehension for standard keys
            # Ideally we'd use PyYAML but we want to stick to standard lib if possible
            # or assume the environment has it.
            # Let's do a basic parse for now.
            metadata = {}
            for line in yaml_text.split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    metadata[key.strip()] = val.strip()
            return metadata, body
        except:
            return {}, content # Failback
    return {}, content

def construct_frontmatter_string(metadata):
    """Constructs a YAML string from a dictionary."""
    if not metadata:
        return ""
    yaml_lines = ["---"]
    for k, v in metadata.items():
        yaml_lines.append(f"{k}: {v}")
    yaml_lines.append("---\n")
    return "\n".join(yaml_lines)

# --- Tool Functions ---

def read_inbox(vault_path, inbox_rel_path="00_收集箱"):
    """Reads files in the inbox."""
    inbox_full_path = Path(vault_path) / inbox_rel_path

    if not inbox_full_path.exists():
        return {"status": "error", "message": f"Inbox not found at {inbox_full_path}"}

    results = []
    try:
        for file in os.listdir(inbox_full_path):
            if file.lower().endswith(('.md', '.txt')):
                file_path = inbox_full_path / file
                content_preview = read_head_tail(file_path)
                results.append({
                    "filename": file,
                    "path": str(file_path),
                    "content_preview": content_preview
                })
        return {"status": "success", "files": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def move_and_enrich(source_path, dest_folder, vault_root, frontmatter_updates=None, dry_run=False):
    """Moves a file and updates its frontmatter."""

    source = Path(source_path).resolve()
    root = Path(vault_root).resolve()
    dest_dir = root / dest_folder

    if not source.exists():
        return {"status": "error", "message": f"Source file not found: {source}"}

    # Security check: Ensure we are inside the vault
    if not str(source).startswith(str(root)) or not str(dest_dir).startswith(str(root)):
        return {"status": "error", "message": "Security Violation: Operations must be within vault root."}

    # Prepare Content
    try:
        with open(source, 'r', encoding='utf-8') as f:
            full_content = f.read()
    except Exception as e:
         return {"status": "error", "message": f"Read failed: {str(e)}"}

    current_meta, body = extract_frontmatter(full_content)

    # Update Metadata
    if frontmatter_updates:
        # Merge, preferring new updates
        for k, v in frontmatter_updates.items():
            current_meta[k] = v

    # Always ensure 'updated' field
    current_meta['updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_content = construct_frontmatter_string(current_meta) + body

    # Destination Filename Handling
    dest_file = dest_dir / source.name

    # Deduplication / Conflict Check
    if dest_file.exists():
        # Check if identical content
        src_hash = calculate_checksum(source)
        dst_hash = calculate_checksum(dest_file)

        if src_hash == dst_hash:
            if not dry_run:
                os.remove(source) # Dedupe
            return {"status": "success", "action": "deduplicated", "message": "Destination exists and is identical. Removed source."}
        else:
            # Conflict: Rename source to avoid overwrite
            timestamp = int(time.time())
            stem = source.stem
            suffix = source.suffix
            new_filename = f"{stem}_{timestamp}{suffix}"
            dest_file = dest_dir / new_filename
            # Warning added to result

    if dry_run:
        return {
            "status": "success",
            "action": "dry_run",
            "source": str(source),
            "destination": str(dest_file),
            "frontmatter_preview": current_meta
        }

    # Execute Move
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        with open(dest_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

        # Verify write before deleting source
        if dest_file.exists() and dest_file.stat().st_size > 0:
            os.remove(source)
            return {"status": "success", "action": "moved", "new_path": str(dest_file)}
        else:
            return {"status": "error", "message": "Write verification failed. Source not deleted."}

    except Exception as e:
        return {"status": "error", "message": f"Move operation failed: {str(e)}"}


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Read Inbox Command
    parser_read = subparsers.add_parser('read_inbox')
    parser_read.add_argument('--vault-root', required=True)
    parser_read.add_argument('--inbox-folder', default='00_收集箱')

    # Move Command
    parser_move = subparsers.add_parser('move')
    parser_move.add_argument('--source', required=True)
    parser_move.add_argument('--dest-folder', required=True)
    parser_move.add_argument('--vault-root', required=True)
    parser_move.add_argument('--frontmatter', help='JSON string of frontmatter updates')
    parser_move.add_argument('--dry-run', action='store_true')

    args = parser.parse_args()

    if args.command == 'read_inbox':
        print(json.dumps(read_inbox(args.vault_root, args.inbox_folder)))

    elif args.command == 'move':
        fm = {}
        if args.frontmatter:
            try:
                fm = json.loads(args.frontmatter)
            except:
                pass # Fail gracefully or log

        print(json.dumps(move_and_enrich(args.source, args.dest_folder, args.vault_root, fm, args.dry_run)))

if __name__ == "__main__":
    main()
