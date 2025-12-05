import joblib, json
from src.inference.pipeline import run_pipeline
from src.preprocessing.vectorization.vector_builder import get_vector

# Load model + scaler + label mapping
model = joblib.load("models/symptom_classifier.pkl")
scaler = joblib.load("models/scalers/standard_scaler.joblib")

with open("models/label_map.json") as f:
    label_map = json.load(f)

with open("models/vector_schema.json") as f:
    vector_schema = json.load(f)


def predict(text):
    result = run_pipeline(text)

    print("\nINPUT:", text)

    if "symptoms" not in result or result.get("error"):
        print("⚠ No symptoms detected — cannot classify.\n")
        return

    # --- Use the exact same vector builder as training ---
    encoded = get_vector(result["symptoms"], vector_schema)
    ordered_vector = encoded["encoded_vector"]

    # Scale + predict
    X = scaler.transform([ordered_vector])
    pred_index = model.predict(X)[0]

    print("Prediction:", label_map[str(pred_index)])

    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X)[0]
        top3 = sorted(enumerate(probs), key=lambda x: x[1], reverse=True)[:3]

        print("Top 3 probabilities:")
        for idx, p in top3:
            print(f"  {label_map[str(idx)]}: {round(float(p),3)}")


# -------- RUN TESTS ----------
tests = [
    "Child with waddling gait, Gowers sign and enlarged calves",
    "Chronic cough, nasal polyps, recurrent lung infections",
    "Progressive memory loss, jerky movements and mood changes",
    "Severe jaundice, Kayser Fleischer rings and tremor",
    "Bone pain, vaso-occlusive crisis and fatigue",
    "Tall slender build, scoliosis and lens dislocation"
]

for t in tests:
    predict(t)
