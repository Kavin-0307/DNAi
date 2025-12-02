import os
import json

# ------------------------------------------------------------
# Resolve project root (folder containing `models` and `src`)
# src/training/dataset_loader.py  →  src  →  project root
# ------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# ------------------------------------------------------------
# Paths (FINAL WORKING VERSION)
# ------------------------------------------------------------
SCHEMA_FILE = os.path.join(PROJECT_ROOT, "data", "vector_schema.json")
DISEASE_FILE = os.path.join(PROJECT_ROOT, "src", "inference", "diseases_profiles.json")

# Normalize paths
SCHEMA_FILE = os.path.normpath(SCHEMA_FILE)
DISEASE_FILE = os.path.normpath(DISEASE_FILE)

print(" PROJECT ROOT:", PROJECT_ROOT)
print(f"| Exists: {os.path.exists(SCHEMA_FILE)}")
print(f"Exists: {os.path.exists(DISEASE_FILE)}")


def load_dataset():
    """Loads schema and validates dataset."""
    
    with open(SCHEMA_FILE, "r") as f:
        schema = json.load(f)

    valid_symptoms = set(schema["symptom_order"])

    with open(DISEASE_FILE, "r") as f:
        raw_profiles = json.load(f)

    cleaned = {}
    warnings = []

    for disease, symptoms in raw_profiles.items():
        disease_key = disease.lower().replace(" ", "_")
        validated = []

        for s in symptoms:
            s_clean = s.lower().replace(" ", "_")
            if s_clean in valid_symptoms:
                validated.append(s_clean)
            else:
                warnings.append(f"symptom skipped: {s_clean} ({disease})")

        if validated:
            cleaned[disease_key] = sorted(set(validated))

    disease_list = sorted(cleaned.keys())
    return {
        "cleaned_profiles": cleaned,
        "schema": schema,
        "label_to_index": {d:i for i, d in enumerate(disease_list)},
        "index_to_label": {i:d for i, d in enumerate(disease_list)},
        "warnings": warnings
    }
