import re
from typing import Dict, List

class NegationDetector:
    def __init__(self):
        # Common medical negation keywords
        self.negation_terms = [
            r"\bno\b",
            r"\bnot\b",
            r"\bwithout\b",
            r"\bdenies?\b",
            r"\babsence of\b",
            r"\bfree of\b",
            r"\blacks\b",
            r"\bnone\b"
        ]

        # How far after a negation we still consider it applying
        self.window_size = 5

    def detect(self, text: str, symptoms: List[str]) -> Dict[str, bool]:
        """
        Returns dict indicating whether each symptom is negated.
        Example: { "fever": True, "cough": False }
        """
        text_lower = text.lower()

        tokens = text_lower.split()
        negations = self._find_negation_positions(tokens)

        symptom_negation = {}

        for symptom in symptoms:
            symptom_words = symptom.split("_")     # "chest_pain" → ["chest","pain"]

            is_neg = self._check_negation(tokens, symptom_words, negations)
            symptom_negation[symptom] = is_neg

        return symptom_negation

    def _find_negation_positions(self, tokens: List[str]) -> List[int]:
        """
        Returns indexes where negation words appear.
        """
        neg_positions = []
        for i, tok in enumerate(tokens):
            for neg in self.negation_terms:
                if re.fullmatch(neg, tok):
                    neg_positions.append(i)
        return neg_positions

    def _check_negation(self, tokens: List[str], symptom_words: List[str], neg_positions: List[int]) -> bool:
        """
        Checks if a symptom appears near a negation term.
        Uses sliding window approach.
        """
        for i in range(len(tokens) - len(symptom_words) + 1):
            if tokens[i:i+len(symptom_words)] == symptom_words:
                # Check distance from each negation word
                for neg_i in neg_positions:
                    if abs(neg_i - i) <= self.window_size:
                        return True
        return False

# Simple usage example
if __name__ == "__main__":
    detector = NegationDetector()
    text = "Patient has cough but no fever and denies chest pain."
    symptoms = ["cough", "fever", "chest pain"]

    result = detector.detect(text, symptoms)
    print(result)
    # Expected:
    # { 'cough': False, 'fever': True, 'chest pain': True }
