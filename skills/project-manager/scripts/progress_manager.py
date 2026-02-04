import os
import sys
import argparse
import datetime

class ProgressManager:
    """
    Manages the progress.md file in a project.
    """
    def __init__(self, project_path):
        self.project_path = project_path
        self.progress_file = os.path.join(project_path, "progress.md")

    def ensure_file(self):
        if not os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'w', encoding='utf-8') as f:
                    f.write(f"# Project Progress\nCreated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n## Tasks\n")
                print(f"Created progress.md at {self.progress_file}")
            except Exception as e:
                print(f"Error creating file: {e}", file=sys.stderr)
                sys.exit(1)

    def add_task(self, task, status="TODO"):
        self.ensure_file()
        try:
            with open(self.progress_file, 'a', encoding='utf-8') as f:
                mark = 'x' if status == 'DONE' else ' '
                f.write(f"- [{mark}] {task}\n")
            print(f"Added task: {task}")
        except Exception as e:
            print(f"Error adding task: {e}", file=sys.stderr)

    def read_progress(self):
        if not os.path.exists(self.progress_file):
            return "No progress.md found."
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"

def main():
    parser = argparse.ArgumentParser(description="Manage progress.md")
    parser.add_argument("project_path", help="Path to project root")
    parser.add_argument("--action", choices=["init", "add", "read"], required=True)
    parser.add_argument("--task", help="Task description")
    parser.add_argument("--status", choices=["TODO", "DONE"], default="TODO")

    args = parser.parse_args()

    manager = ProgressManager(args.project_path)

    if args.action == "init":
        manager.ensure_file()
    elif args.action == "add":
        if not args.task:
            print("Error: --task required for add", file=sys.stderr)
            sys.exit(1)
        manager.add_task(args.task, args.status)
    elif args.action == "read":
        print(manager.read_progress())

if __name__ == "__main__":
    main()
