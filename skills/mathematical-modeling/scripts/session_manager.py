import json
import os
from typing import Dict, Any, Optional

class BaseSessionManager:
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        # Uses .claude-temp for temporary storage as per DR-002/009 conventions
        self.storage_dir = os.path.join(os.getcwd(), ".claude-temp", "math_modeling_sessions")
        os.makedirs(self.storage_dir, exist_ok=True)
        self.file_path = os.path.join(self.storage_dir, f"{self.session_id}.json")
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save(self) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def update_context(self, key: str, value: Any) -> None:
        self.data[key] = value
        self.save()

    def get_context(self, key: str) -> Optional[Any]:
        return self.data.get(key)

    def clear(self) -> None:
        self.data = {}
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

# Singleton instance for the skill
session = BaseSessionManager()
