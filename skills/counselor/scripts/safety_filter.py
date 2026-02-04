import re

class SafetyFilter:
    def __init__(self):
        # Regex patterns for PII
        self.patterns = {
            "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            "phone_cn": r'(?<!\d)(?:(?:\+|00)86)?1[3-9]\d{9}(?!\d)',
            "phone_simple": r'(?<!\d)\d{3}[-.\s]?\d{3}[-.\s]?\d{4}(?!\d)'
        }

    def sanitize(self, text: str) -> str:
        """Redacts PII from the input text."""
        sanitized_text = text

        # Redact Emails
        sanitized_text = re.sub(self.patterns["email"], "[EMAIL_REDACTED]", sanitized_text)

        # Redact Phones
        sanitized_text = re.sub(self.patterns["phone_cn"], "[PHONE_REDACTED]", sanitized_text)
        sanitized_text = re.sub(self.patterns["phone_simple"], "[PHONE_REDACTED]", sanitized_text)

        return sanitized_text
