import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

SYMPTOM_DICT = os.path.join(PROJECT_ROOT, "src", "preprocessing", "vectorization", "symptom_dictionary.json")

SCHEMA_FILE = os.path.join(PROJECT_ROOT, "models", "vector_schema.json")
SCHEMA_FILE = os.path.normpath(SCHEMA_FILE)

print(f"\n Loading schema from:\n   {SCHEMA_FILE}")

# Load schema file
with open(SCHEMA_FILE, "r") as f:
    schema = json.load(f)

# Load symptom dictionary
with open(SYMPTOM_DICT, "r") as f:
    symptom_dict = json.load(f)

# Update sorted symptom order
schema["symptom_order"] = sorted(symptom_dict.keys())

# Save back updated schema
with open(SCHEMA_FILE, "w") as f:
    json.dump(schema, f, indent=4)

print("\n Schema updated successfully!")
print(f" Total symptoms inserted: {len(schema['symptom_order'])}")
print("\nDone.\n")
