import unittest
import tempfile
import shutil
import os
import sys

# Add scripts to path for testing
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_path = os.path.join(current_dir, "..", "scripts")
sys.path.append(scripts_path)

from project_scanner import scan_directory
from progress_manager import ProgressManager

class TestProjectManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_scan_directory(self):
        # Create some files
        os.makedirs(os.path.join(self.test_dir, "src"))
        with open(os.path.join(self.test_dir, "README.md"), "w") as f:
            f.write("test")

        result = scan_directory(self.test_dir)

        self.assertEqual(result["root"], os.path.abspath(self.test_dir))
        self.assertIn("README.md", result["key_files"][0])

        # Check structure
        root_struct = next((item for item in result["structure"] if item["path"] == ""), None)
        self.assertIsNotNone(root_struct)
        self.assertIn("src", root_struct["dirs"])

    def test_progress_manager(self):
        manager = ProgressManager(self.test_dir)

        # Test Init
        manager.ensure_file()
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "progress.md")))

        # Test Add
        manager.add_task("Test Task 1")
        content = manager.read_progress()
        self.assertIn("- [ ] Test Task 1", content)

        # Test Add Done
        manager.add_task("Test Task 2", status="DONE")
        content = manager.read_progress()
        self.assertIn("- [x] Test Task 2", content)

if __name__ == "__main__":
    unittest.main()
