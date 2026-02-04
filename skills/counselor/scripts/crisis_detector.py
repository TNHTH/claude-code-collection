import typing

class CrisisDetector:
    def __init__(self):
        self.risk_keywords = [
            "suicide", "kill myself", "die", "end my life",
            "自杀", "不想活了", "结束生命", "去死", "自我了断",
            "hurt myself", "cutting myself", "割腕"
        ]

    def detect(self, text: str) -> dict:
        """
        Checks text for crisis keywords.
        Returns a dict with safety status and detected triggers.
        """
        text_lower = text.lower()
        detected = [kw for kw in self.risk_keywords if kw in text_lower]

        is_crisis = len(detected) > 0

        return {
            "is_crisis": is_crisis,
            "detected_keywords": detected,
            "safety_message": "CRISIS DETECTED: Please stop immediately and provide emergency resources." if is_crisis else "Safe"
        }
