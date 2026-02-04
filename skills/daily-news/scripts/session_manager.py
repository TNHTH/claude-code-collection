import os
import json
import argparse
import datetime
import sys

# Constants based on analysis
# Assuming the script is run from the project root
BASE_DIR = os.path.join("Si Yuan", "世界变化")
STATE_FILE = os.path.join(BASE_DIR, ".daily-news-state.json")
OUTPUT_BASE_DIR = os.path.join(BASE_DIR, "每日时事")

def ensure_directory(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            # print(f"Created directory: {path}") # Reduce noise
        except OSError as e:
            print(f"Error creating directory {path}: {e}", file=sys.stderr)
            sys.exit(1)

def get_today_path():
    """Returns the canonical output path for today's news."""
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    weekday_map = {0: "一", 1: "二", 2: "三", 3: "四", 4: "五", 5: "六", 6: "日"}
    weekday = weekday_map[now.weekday()]

    # Format: Si Yuan/世界变化/每日时事/{YYYY}年{M}月/{YYYY}年{M}月{D}日（周{X}）.md
    month_dir = os.path.join(OUTPUT_BASE_DIR, f"{year}年{month}月")
    filename = f"{year}年{month}月{day}日（周{weekday}）.md"
    full_path = os.path.join(month_dir, filename)

    ensure_directory(month_dir)
    return full_path

def read_state():
    """Safely reads the state file."""
    # Ensure base dir exists for state file
    ensure_directory(BASE_DIR)

    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: State file {STATE_FILE} is corrupted. Returning empty state.", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"Error reading state file: {e}", file=sys.stderr)
        return {}

def update_state(key, value):
    """Updates a key in the state file."""
    ensure_directory(BASE_DIR)
    state = read_state()

    # Handle timestamp automatically
    state['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state[key] = value

    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        print(f"State updated: {key} = {value}")
    except Exception as e:
        print(f"Error updating state file: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Session Manager for Daily News Skill")
    parser.add_argument("--action", required=True, choices=["get_path", "read_state", "update_state"])
    parser.add_argument("--key", help="Key for update_state")
    parser.add_argument("--value", help="Value for update_state")

    args = parser.parse_args()

    if args.action == "get_path":
        print(get_today_path())
    elif args.action == "read_state":
        print(json.dumps(read_state(), ensure_ascii=False, indent=2))
    elif args.action == "update_state":
        if not args.key:
            print("Error: --key is required for update_state", file=sys.stderr)
            sys.exit(1)
        # Value is optional, could be null/None if clearing, but for now let's assume value is needed or default to empty string
        val = args.value if args.value is not None else ""
        update_state(args.key, val)

if __name__ == "__main__":
    main()
