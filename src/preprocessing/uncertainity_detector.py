import re
from typing import Dict, List

class UncertaintyDetector:
    def __init__(self):
        # Common uncertainty terms in clinical text
        self.uncertainty_terms = [
            r"\bpossible\b",
            r"\bpossibly\b",
            r"\bmight\b",
            r"\bmay\b",
            r"\blikely\b",
            r"\bsuspected\b",
            r"\bconcern for\b",
            r"\brule out\b",
            r"\br/o\b",
            r"\bquestion of\b",
            r"\b?\b"   # doctors often write "?tb"
        ]

        self.window_size = 5

    def detect(self, text: str, symptoms: List[str]) -> Dict[str, bool]:
        text_lower = text.lower()
        tokens = text_lower.split()

        uncertain_positions = self._find_uncertainty_positions(tokens)
        symptom_uncertainty = {}

        for symptom in symptoms:
            symptom_words = symptom.split("_")
            is_uncertain = self._check_uncertainty(tokens, symptom_words, uncertain_positions)
            symptom_uncertainty[symptom] = is_uncertain

        return symptom_uncertainty

    def _find_uncertainty_positions(self, tokens: List[str]) -> List[int]:
        positions = []
        for i, tok in enumerate(tokens):
            for term in self.uncertainty_terms:
                if re.fullmatch(term, tok):
                    positions.append(i)
        return positions

    def _check_uncertainty(self, tokens, symptom_words, uncertain_positions):
        for i in range(len(tokens) - len(symptom_words) + 1):
            if tokens[i:i+len(symptom_words)] == symptom_words:
                # Check if uncertainty word is nearby
                for u_i in uncertain_positions:
                    if abs(u_i - i) <= self.window_size:
                        return True
        return False
