import json
import re
from pathlib import Path


class ConceptNormalizer:
    def __init__(self, dictionary_path: str):
        self.dictionary_path = dictionary_path
        self.symptom_map = self._load_dictionary()
        self.inverse_index = self._build_inverse_index()

    # Load base dictionary
    def _load_dictionary(self):
        with open(self.dictionary_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # Build inverse lookup table
    def _build_inverse_index(self):
        inverse = {}

        for canonical, synonyms in self.symptom_map.items():
            # add the canonical itself
            inverse[self._clean(canonical)] = canonical

            # add all synonyms
            for s in synonyms:
                inverse[self._clean(s)] = canonical

        return inverse

   
    # Helper: minimal cleaning
    def _clean(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        return text

    # Public: Normalize extracted symptoms

    def normalize_symptoms(self, extracted_symptoms: dict):
        """
        Input:
            {"severe cough": {"severity":0.8, "duration":14}}
        Output:
            {"chronic_cough": {"severity":0.8, "duration":14}}
        """

        normalized = {}

        for raw_name, values in extracted_symptoms.items():
            cleaned = self._clean(raw_name)

            if cleaned in self.inverse_index:
                canonical = self.inverse_index[cleaned]
            else:
                # optional: keep unknowns separately
                canonical = raw_name  

            if canonical not in normalized:
                normalized[canonical] = values
            else:
                # merge duplicates → keep higher severity / longer duration
                normalized[canonical]["severity"] = max(
                    normalized[canonical]["severity"],
                    values.get("severity", 0)
                )
                normalized[canonical]["duration"] = max(
                    normalized[canonical]["duration"],
                    values.get("duration", 0)
                )

        return normalized
