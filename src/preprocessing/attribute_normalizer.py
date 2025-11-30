import re

class AttributeNormalizer:
    """
    Normalizes severity, duration, frequency, laterality, temporal cues,
    and progression/worsening indicators for each symptom.
    """

    SEVERITY_KEYWORDS = {
        "mild": 0.3,
        "moderate": 0.6,
        "severe": 0.9,
        "very severe": 1.0,
        "extremely severe": 1.0
    }

    TEMPORAL_CUES = {
        "acute": "acute",
        "sudden": "acute",
        "chronic": "chronic",
        "long-term": "chronic",
        "persistent": "chronic",
        "intermittent": "intermittent"
    }

    LATERALITY = {
        "left": "left",
        "right": "right",
        "bilateral": "bilateral"
    }

    FREQUENCY = {
        "rarely": 0.2,
        "sometimes": 0.4,
        "often": 0.7,
        "frequently": 0.8,
        "constantly": 1.0
    }

    def __init__(self):
        pass

    # Severity extractor

    def normalize_severity(self, text: str, default=0.5):
        text = text.lower()
        for phrase, value in self.SEVERITY_KEYWORDS.items():
            if phrase in text:
                return value
        return default

    # Frequency extractor
    def normalize_frequency(self, text: str):
        text = text.lower()
        for phrase, value in self.FREQUENCY.items():
            if phrase in text:
                return value
        return None

    # Laterality extractor
    def normalize_laterality(self, text: str):
        text = text.lower()
        for lat in self.LATERALITY:
            if lat in text:
                return self.LATERALITY[lat]
        return None

    # Temporal cue extractor
    def normalize_temporal(self, text: str):
        text = text.lower()
        for cue in self.TEMPORAL_CUES:
            if cue in text:
                return self.TEMPORAL_CUES[cue]
        return None

    # Progression extractor (worsening/improving)
    def normalize_progression(self, text: str):
        text = text.lower()

        if any(word in text for word in ["worsening", "increasing", "getting worse"]):
            return "worsening"

        if any(word in text for word in ["improving", "getting better"]):
            return "improving"

        return None

    # Main function
    def normalize_attributes(self, symptom_text: str):
        """Returns all normalized attributes for a symptom"""
        return {
            "severity": self.normalize_severity(symptom_text),
            "frequency": self.normalize_frequency(symptom_text),
            "laterality": self.normalize_laterality(symptom_text),
            "temporal_cue": self.normalize_temporal(symptom_text),
            "progression": self.normalize_progression(symptom_text)
        }
