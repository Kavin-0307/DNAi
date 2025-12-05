"""
import json
import random
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILE = PROJECT_ROOT / "data" / "synthetic" / "n1_training_cases.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "synthetic" / "augmented_training_cases.json"

TARGET_COUNT = 12  # << you set this


# Lightweight controlled phrase variations
TEMPLATES = [
    "{symptoms} suggest {disease}.",
    "Patient presents with {symptoms}, which is consistent with {disease}.",
    "A case showing {symptoms}, likely {disease}.",
    "Symptoms including {symptoms} point toward {disease}.",
    "This patient shows {symptoms}, typically seen in {disease}.",
    "{symptoms}. Diagnosis leaning toward {disease}.",
]

# Synonym/phrase variation so symptoms shift wording
REPHRASE = [
    lambda s: s,
    lambda s: s.replace("and", ","),
    lambda s: "Symptoms include " + s,
    lambda s: "Presence of " + s,
]


def load_cases():
    with open(SOURCE_FILE, "r") as f:
        return json.load(f)


def group_cases_by_disease(cases):
    grouped = {}
    for case in cases:
        grouped.setdefault(case["disease"], []).append(case)
    return grouped


def augment_sentence(text):
    
    text = text.strip()
    if random.random() < 0.3:
        text = text.replace("patient", "child").replace("Patient", "Child")
    
    if random.random() < 0.25:
        text = "Reported case: " + text.lower()
    
    return text


def create_augmented_case(base_case):
    disease = base_case["disease"]
    original = base_case["text"]

    # Extract list of symptoms (comma split fallback)
    parts = original.lower().replace(".", "").split(",")
    symptoms_str = ", ".join([p.strip() for p in parts[:3]])

    template = random.choice(TEMPLATES)
    phrased_symptoms = random.choice(REPHRASE)(symptoms_str)

    new_text = template.format(symptoms=phrased_symptoms, disease=disease)
    new_text = augment_sentence(new_text)

    return {"disease": disease, "text": new_text}


def generate_balanced_dataset():
    original_cases = load_cases()
    grouped = group_cases_by_disease(original_cases)

    final_cases = original_cases.copy()

    for disease, cases in grouped.items():
        shortfall = TARGET_COUNT - len(cases)

        if shortfall > 0:
            print(f"➡️ {disease} needs {shortfall} more samples. Generating...")
            for _ in range(shortfall):
                base = random.choice(cases)
                final_cases.append(create_augmented_case(base))
        else:
            print(f"✔ {disease} already has {len(cases)}, no augmentation needed.")

    return final_cases


if __name__ == "__main__":
    result = generate_balanced_dataset()

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n🎉 Augmentation complete — final count: {len(result)} saved to:")
    print(OUTPUT_FILE)
"""""