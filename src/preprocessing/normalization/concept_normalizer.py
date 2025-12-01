import json
import re
import os
from pathlib import Path


class ConceptNormalizer:
    def __init__(self, dictionary_path: str | None = None):
        self.dictionary_path = dictionary_path
        self.symptom_map = self._load_dictionary()
        self.inverse_index = self._build_inverse_index()

    # Dictionary loader
    def _load_dictionary(self):
        if not self.dictionary_path or not os.path.exists(self.dictionary_path):
            print(f"[ConceptNormalizer] No dictionary found at: {self.dictionary_path} — using empty mapping.")
            return {}  # prevent crash

        with open(self.dictionary_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _build_inverse_index(self):
        inverse = {}

        for canonical, synonyms in self.symptom_map.items():
            # canonical name maps to itself
            inverse[self._clean(canonical)] = canonical

            # synonyms map to canonical
            for word in synonyms:
                inverse[self._clean(word)] = canonical

        return inverse

   
    def _clean(self, text: str) -> str:
        text = text.lower().strip()
        return re.sub(r"[^a-z0-9\s]", "", text)

  
    def normalize_symptoms(self, extracted: dict) -> dict:
        """
        Example:
            input:  {"severe coughing": {...}}
            output: {"cough": {...}}
        """
        normalized = {}

        for raw_name, values in extracted.items():
            cleaned = self._clean(raw_name)

            if cleaned in self.inverse_index:
                canonical = self.inverse_index[cleaned]
            else:
                canonical = raw_name  # fallback if unknown

            if canonical not in normalized:
                normalized[canonical] = values
            else:
                # merge logic: keep highest severity, longest duration
                normalized[canonical]["severity"] = max(
                    normalized[canonical].get("severity", 0),
                    values.get("severity", 0)
                )
                normalized[canonical]["duration_days"] = max(
                    normalized[canonical].get("duration_days", 0),
                    values.get("duration_days", 0)
                )

        return normalized



BASE_DIR = Path(__file__).resolve().parent.parent.parent  # goes to /src
DEFAULT_DICT_PATH = BASE_DIR / "data" / "concept_dictionary.json"

normalizer = ConceptNormalizer(str(DEFAULT_DICT_PATH))



def normalize_concepts(symptom_dict: dict) -> dict:
    """
    This is what the pipeline calls.
    """
    return normalizer.normalize_symptoms(symptom_dict)
