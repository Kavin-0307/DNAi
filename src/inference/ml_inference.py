import numpy as np
import json
from pathlib import Path
from .rule_engine import apply_rules
import joblib

# ==== LOAD STATIC MODEL ASSETS ====
label_map = json.loads(Path("models/label_map.json").read_text())
vector_schema = json.loads(Path("models/vector_schema.json").read_text())
model = joblib.load("models/symptom_classifier.pkl")
scaler = joblib.load("models/scalers/standard_scaler.joblib")


def normalize(scores: dict) -> dict:
    total = sum(scores.values())
    if total > 0:
        return {k: v / total for k, v in scores.items()}
    return scores


def get_top_weighted_symptoms(disease_index, top_n=5):
    """Extract model-learned strongest positive symptom features."""
    weights = model.coef_[disease_index]
    symptom_names = list(vector_schema.keys())

    top_indices = np.argsort(weights)[::-1][:top_n]

    return [symptom_names[i] for i in top_indices if weights[i] > 0.01]


def fused_predict(encoded_vector, extracted_symptoms):
    """Hybrid ML + rule-based inference with interpretability."""
    X = scaler.transform([encoded_vector])
    probas = model.predict_proba(X)[0]
    ml_scores = {label_map[str(i)]: float(probas[i]) for i in range(len(probas))}

    rule_scores = apply_rules(ml_scores, extracted_symptoms)

    fused = {
        disease: (0.6 * ml_scores[disease] + 0.4 * rule_scores[disease])
        for disease in ml_scores
    }

    fused = normalize(fused)

    # --- TOP CANDIDATES ---
    top_results = sorted(fused.items(), key=lambda x: x[1], reverse=True)[:3]

    response = []

    for disease, score in top_results:
        idx = list(label_map.values()).index(disease)
        key_symptoms = get_top_weighted_symptoms(idx)

        matched = list(set(key_symptoms).intersection(set(extracted_symptoms)))

        response.append({
            "disease": disease,
            "score": round(score, 3),
            "confidence": score_to_label(score),
            "matching_key_symptoms": matched,
            "missing_key_symptoms": [s for s in key_symptoms if s not in matched],
        })

    return response


def score_to_label(s):
    if s >= 0.75: return "HIGH "
    if s >= 0.50: return "MODERATE "
    if s >= 0.30: return "LOW "
    return "VERY LOW "
