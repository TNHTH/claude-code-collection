import sys
import os
import json
from datetime import datetime
from typing import Dict, Any, List

# Add shared scripts to path
current_dir = os.path.dirname(os.path.abspath(__file__))
shared_dir = os.path.abspath(os.path.join(current_dir, "../../../shared/scripts"))
if shared_dir not in sys.path:
    sys.path.append(shared_dir)

try:
    from session_manager import BaseSessionManager
except ImportError:
    # Fallback mock for independent testing if shared not available
    class BaseSessionManager:
        def __init__(self, base_dir, state_file_name): pass
        def update_state(self, updates): pass
        def get_value(self, key, default): return default

class CounselorSessionManager(BaseSessionManager):
    def __init__(self, base_dir: str = ".claude/skills/counselor"):
        # Ensure base_dir is absolute or relative to CWD correctly
        if not os.path.isabs(base_dir):
             base_dir = os.path.abspath(base_dir)

        super().__init__(base_dir, "session_state.json")
        self.history_file = os.path.join(self.base_dir, "session_history.jsonl")

    def start_session(self, user_id: str = "default") -> str:
        """Starts a new counseling session."""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.update_state({
            "current_session_id": session_id,
            "session_start": datetime.now().isoformat(),
            "user_id": user_id,
            "status": "active"
        })
        return session_id

    def log_interaction(self, input_text: str, output_text: str, sentiment: str = "neutral") -> None:
        """Logs a single interaction to history (append-only)."""
        session_id = self.get_value("current_session_id", "unknown")
        entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "input": input_text,
            "output": output_text,
            "sentiment": sentiment
        }

        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def end_session(self) -> None:
        """Ends the current session."""
        self.update_state({
            "status": "completed",
            "session_end": datetime.now().isoformat()
        })
