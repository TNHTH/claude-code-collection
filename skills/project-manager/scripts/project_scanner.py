import os
import json
import argparse
import sys

def scan_directory(path, max_depth=3):
    """
    Scans a directory to provide a summary structure and identify key files.
    """
    path = os.path.abspath(path)
    if not os.path.exists(path):
        return {"error": f"Path {path} does not exist"}

    structure = []
    key_files = []
    errors = []

    # Common configuration and documentation files
    KEY_FILE_NAMES = {
        'README.md', 'package.json', 'requirements.txt', '.env.example', '.env',
        'pom.xml', 'build.gradle', 'Makefile', 'Dockerfile', 'docker-compose.yml',
        'CLAUDE.md', 'go.mod', 'Cargo.toml', 'tsconfig.json', 'pyproject.toml'
    }

    base_depth = path.rstrip(os.sep).count(os.sep)

    def walk_error_handler(e):
        try:
            errors.append(f"Error accessing {e.filename}: {e.strerror}")
        except:
            errors.append(str(e))

    try:
        # Use onerror callback for os.walk to handle permission errors gracefully
        for root, dirs, files in os.walk(path, onerror=walk_error_handler):
            try:
                # Calculate current depth
                current_depth = root.rstrip(os.sep).count(os.sep) - base_depth

                # Don't traverse deeper than max_depth
                if current_depth > max_depth:
                    del dirs[:]
                    continue

                # Ignore hidden folders (start with .)
                dirs[:] = [d for d in dirs if not d.startswith('.')]

                rel_path = os.path.relpath(root, path)
                if rel_path == '.':
                    rel_path = ''

                folder_info = {
                    "path": rel_path,
                    "files": [f for f in files if not f.startswith('.')],
                    "dirs": dirs
                }
                structure.append(folder_info)

                for f in files:
                    if f in KEY_FILE_NAMES:
                        key_files.append(os.path.join(rel_path, f))
            except Exception as e:
                errors.append(f"Error processing directory {root}: {str(e)}")

    except Exception as e:
        return {"error": f"Critical error scanning path: {str(e)}"}

    return {
        "root": path,
        "key_files": key_files,
        "structure": structure[:50], # Limit output size for LLM context window
        "errors": errors if errors else None
    }

def main():
    parser = argparse.ArgumentParser(description="Scan project directory")
    parser.add_argument("path", help="Project path to scan")
    parser.add_argument("--max-depth", type=int, default=3, help="Max depth to scan")
    parser.add_argument("--fast", action="store_true", help="Fast mode (sets max-depth to 2)")
    args = parser.parse_args()

    depth = args.max_depth
    if args.fast:
        depth = 2

    result = scan_directory(args.path, depth)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
