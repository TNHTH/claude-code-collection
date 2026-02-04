import os
import json
import sys
import datetime
from typing import Any, Dict, Optional

class BaseSessionManager:
    """
    A robust session manager for handling state persistence across tool invocations.
    """
    def __init__(self, base_dir: str, state_file_name: str):
        self.base_dir = os.path.abspath(base_dir)
        self.state_file = os.path.join(self.base_dir, state_file_name)
        self.ensure_directory(self.base_dir)

    def ensure_directory(self, path: str) -> None:
        """Ensures the directory exists, creating it if necessary."""
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as e:
                print(f"Error creating directory {path}: {e}", file=sys.stderr)
                raise

    def read_state(self) -> Dict[str, Any]:
        """Reads the state from the JSON file."""
        if not os.path.exists(self.state_file):
            return {}
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: State file {self.state_file} is corrupted. Returning empty state.", file=sys.stderr)
            return {}
        except Exception as e:
            print(f"Error reading state file: {e}", file=sys.stderr)
            return {}

    def update_state(self, updates: Dict[str, Any]) -> None:
        """Updates the state file with new values."""
        state = self.read_state()
        state['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        state.update(updates)

        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error updating state file: {e}", file=sys.stderr)
            raise

    def get_value(self, key: str, default: Any = None) -> Any:
        """Retrieves a specific value from the state."""
        state = self.read_state()
        return state.get(key, default)
