import sys
import os
import argparse

# Add shared scripts to path
current_dir = os.path.dirname(os.path.abspath(__file__))
shared_path = os.path.join(current_dir, "..", "..", "shared", "scripts")
sys.path.append(shared_path)

try:
    from session_manager import BaseSessionManager
except ImportError:
    print(f"Error: Could not import BaseSessionManager from {shared_path}", file=sys.stderr)
    sys.exit(1)

class ProjectSessionManager(BaseSessionManager):
    """
    Manages project-specific state such as the current active project.
    """
    def __init__(self, base_dir=None):
        # Default to .claude-temp/project-manager if not specified
        if not base_dir:
             base_dir = os.path.join(os.getcwd(), ".claude-temp", "project-manager")
        super().__init__(base_dir, "project_state.json")

    def set_current_project(self, project_path):
        self.update_state({"current_project": os.path.abspath(project_path)})

    def get_current_project(self):
        return self.get_value("current_project")

def main():
    parser = argparse.ArgumentParser(description="Project Session Manager")
    parser.add_argument("action", choices=["init", "get", "set"])
    parser.add_argument("--project-path", help="Path to the project (required for 'set')")

    args = parser.parse_args()

    manager = ProjectSessionManager()

    if args.action == "init":
        print(f"Session initialized at {manager.base_dir}")
    elif args.action == "set":
        if not args.project_path:
            print("Error: --project-path required for set", file=sys.stderr)
            sys.exit(1)
        manager.set_current_project(args.project_path)
        print(f"Current project set to: {os.path.abspath(args.project_path)}")
    elif args.action == "get":
        project = manager.get_current_project()
        if project:
            print(project)
        else:
            print("No project set.")

if __name__ == "__main__":
    main()
