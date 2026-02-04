import os
import json
import datetime
import argparse
from pathlib import Path

# Configuration
EXCLUDE_DIRS = {'.git', '.obsidian', '.claude', '.claude-temp', '.trash', 'node_modules'}
EXTENSIONS = {'.md', '.canvas', '.txt'}

def scan_vault(vault_root, max_depth=5):
    """
    Scans the vault and returns a structure dictionary.
    """
    vault_path = Path(vault_root).resolve()
    structure = {
        "last_updated": datetime.datetime.now().isoformat(),
        "structure": {
            "folders": []
        },
        "file_map": {},
        "tags": {}  # Placeholder for future tag indexing if needed
    }

    # Walk the directory
    for root, dirs, files in os.walk(vault_path):
        # Modify dirs in-place to skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        rel_path = Path(root).relative_to(vault_path)

        # Check depth
        if len(rel_path.parts) > max_depth:
            continue

        # Add folder to structure (use forward slashes for consistency)
        folder_str = str(rel_path).replace('\\', '/')
        if folder_str != '.':
            structure["structure"]["folders"].append(folder_str)

        # Process files
        for file in files:
            if Path(file).suffix.lower() in EXTENSIONS:
                file_path = Path(root) / file
                rel_file_path = str(file_path.relative_to(vault_path)).replace('\\', '/')

                # key is filename, value is relative path
                # Note: This simple map might overwrite if filenames are duplicate.
                # For an organizer, usually unique filenames are preferred,
                # or we could use a list of paths for duplicates.
                if file in structure["file_map"]:
                    # If duplicate, make it a list or append
                    current = structure["file_map"][file]
                    if isinstance(current, list):
                        current.append(rel_file_path)
                    else:
                        structure["file_map"][file] = [current, rel_file_path]
                else:
                    structure["file_map"][file] = rel_file_path

    return structure

def main():
    parser = argparse.ArgumentParser(description='Scan Obsidian Vault and build index.')
    parser.add_argument('--vault-path', required=True, help='Root path of the Obsidian vault')
    parser.add_argument('--output', required=True, help='Path to save the JSON index')
    parser.add_argument('--max-depth', type=int, default=10, help='Maximum folder depth to scan')

    args = parser.parse_args()

    try:
        data = scan_vault(args.vault_path, args.max_depth)

        # Ensure output directory exists
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(json.dumps({"status": "success", "message": f"Index built with {len(data['file_map'])} files.", "path": str(output_path)}))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    main()
