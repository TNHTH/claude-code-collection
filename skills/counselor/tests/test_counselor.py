import unittest
import sys
import os

# Add scripts directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from safety_filter import SafetyFilter
from crisis_detector import CrisisDetector

class TestCounselorSkill(unittest.TestCase):
    def setUp(self):
        self.safety = SafetyFilter()
        self.detector = CrisisDetector()

    def test_pii_redaction(self):
        text = "My email is test@example.com and phone is 13800138000."
        sanitized = self.safety.sanitize(text)
        self.assertIn("[EMAIL_REDACTED]", sanitized)
        self.assertIn("[PHONE_REDACTED]", sanitized)
        self.assertNotIn("test@example.com", sanitized)
        self.assertNotIn("13800138000", sanitized)

    def test_crisis_detection_safe(self):
        text = "I feel sad today."
        result = self.detector.detect(text)
        self.assertFalse(result["is_crisis"])

    def test_crisis_detection_danger_en(self):
        text = "I want to kill myself."
        result = self.detector.detect(text)
        self.assertTrue(result["is_crisis"])
        self.assertIn("kill myself", result["detected_keywords"])

    def test_crisis_detection_danger_cn(self):
        text = "我真的不想活了。"
        result = self.detector.detect(text)
        self.assertTrue(result["is_crisis"])
        self.assertIn("不想活了", result["detected_keywords"])

if __name__ == '__main__':
    unittest.main()
