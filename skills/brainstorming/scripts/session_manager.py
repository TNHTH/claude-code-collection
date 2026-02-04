import sys
import os
import uuid
from datetime import datetime
from typing import List, Dict, Any

# 添加 shared scripts 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../shared/scripts')))
try:
    from session_manager import BaseSessionManager
except ImportError:
    # Fallback for testing environment
    class BaseSessionManager:
        def __init__(self, base_dir, state_file_name): pass
        def update_state(self, updates): pass
        def get_value(self, key, default): return default

class BrainstormingSession(BaseSessionManager):
    def __init__(self):
        # 状态存储在 .claude-temp/brainstorming
        super().__init__(
            base_dir=os.path.abspath(os.path.join(os.getcwd(), '.claude-temp', 'brainstorming')),
            state_file_name='current_session.json'
        )

    def start_new_session(self, topic: str):
        self.update_state({
            'session_id': str(uuid.uuid4()),
            'topic': topic,
            'stage': 'diverge',  # diverge -> converge -> rank
            'ideas': [],
            'created_at': datetime.now().isoformat()
        })

    def add_ideas(self, ideas: List[str]):
        current_ideas = self.get_value('ideas', [])
        new_entries = [
            {
                'id': str(uuid.uuid4())[:8],
                'text': text,
                'ice': {'i': 0, 'c': 0, 'e': 0},
                'score': 0
            } for text in ideas
        ]
        self.update_state({'ideas': current_ideas + new_entries})

    def get_ideas(self) -> List[Dict]:
        return self.get_value('ideas', [])

    def update_stage(self, stage: str):
        self.update_state({'stage': stage})
