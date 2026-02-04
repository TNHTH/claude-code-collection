import unittest
import os
import sys
import json
import shutil
from unittest.mock import patch

# Add scripts directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
import session_manager

class TestSessionManager(unittest.TestCase):
    def test_get_today_path_structure(self):
        # Check that the path generated adheres to the expected structure
        path = session_manager.get_today_path()

        # Check components
        self.assertIn(os.path.join("Si Yuan", "世界变化", "每日时事"), path)
        self.assertTrue(path.endswith(".md"))

        # Check that the directory was actually created (Poka-Yoke)
        dir_path = os.path.dirname(path)
        self.assertTrue(os.path.exists(dir_path))

    def test_read_write_state(self):
        # Use a temporary state file for testing
        test_state_file = "test_daily_news_state.json"

        # Mock the STATE_FILE constant in the module
        with patch('session_manager.STATE_FILE', test_state_file):
            # 1. Clean up potential leftovers
            if os.path.exists(test_state_file):
                os.remove(test_state_file)

            # 2. Test reading non-existent file (should return empty dict, not crash)
            state = session_manager.read_state()
            self.assertEqual(state, {})

            # 3. Test updating state
            session_manager.update_state("test_user", "automation_student")

            # 4. Test reading back
            new_state = session_manager.read_state()
            self.assertEqual(new_state["test_user"], "automation_student")
            self.assertIn("last_updated", new_state)

            # Cleanup
            if os.path.exists(test_state_file):
                os.remove(test_state_file)

if __name__ == '__main__':
    unittest.main()
