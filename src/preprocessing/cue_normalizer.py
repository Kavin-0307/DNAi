import json
import re
from typing import List, Dict


class CueNormalizer:
    """
    Normalizes cue phrases (onset patterns, triggers, modifiers, progression indicators)
    into standardized internal cue labels.
    """

    def __init__(self, cue_dictionary_path: str = "data/cue_dictionary.json"):
        self.cue_dict = self._load_dictionary(cue_dictionary_path)
        self.reverse_map = self._build_reverse_map()

    def _load_dictionary(self, path: str) -> Dict[str, List[str]]:
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[cue_normalizer] Dictionary missing at {path}, using empty dictionary.")
            return {}

    def _build_reverse_map(self) -> Dict[str, str]:
        reverse = {}
        for canonical, synonyms in self.cue_dict.items():
            for s in synonyms:
                reverse[s.lower()] = canonical
        return reverse

    def normalize(self, extracted_cues: List[str]) -> List[str]:
        normalized = []

        for cue in extracted_cues:
            cleaned = cue.lower().strip()

            # Direct dictionary match
            if cleaned in self.reverse_map:
                normalized.append(self.reverse_map[cleaned])
                continue

            # Fuzzy pattern fallback
            mapped = self._fuzzy_map(cleaned)
            if mapped:
                normalized.append(mapped)

        return list(set(normalized))  # Deduplicate

    def _fuzzy_map(self, phrase: str) -> str:
        phrase = phrase.lower()

        # simple fuzzy: substring match against synonyms
        for canonical, synonyms in self.cue_dict.items():
            for s in synonyms:
                if s in phrase:
                    return canonical
        return None
