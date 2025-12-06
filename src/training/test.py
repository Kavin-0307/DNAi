import joblib, json
from src.inference.pipeline import run_pipeline
from src.preprocessing.vectorization.vector_builder import get_vector

# Load model + scaler + mappings
model = joblib.load("models/symptom_classifier.pkl")
scaler = joblib.load("models/scalers/standard_scaler.joblib")

with open("models/label_map.json") as f:
    label_map = json.load(f)

with open("models/vector_schema.json") as f:
    vector_schema = json.load(f)


def confidence_label(p):
    """Return doctor-friendly confidence level."""
    if p >= 0.75: return "HIGH 🔥"
    if p >= 0.50: return "MODERATE ⚠"
    if p >= 0.30: return "LOW ❓"
    return "VERY LOW ❗"


def predict(text):
    print("\n──────────────────────────────────────────")
    print(f"INPUT > {text}")
    print("──────────────────────────────────────────")

    result = run_pipeline(text)

    if "symptoms" not in result or not result["symptoms"]:
        print("⚠ No recognized symptoms → Cannot classify.\n")
        return

    # --- Show extracted symptoms ---
    detected = result["symptoms"]
    print(f"Extracted symptoms ({len(detected)}):")
    print("  → " + ", ".join(detected))
    print()

    # --- Vectorization ---
    encoded = get_vector(detected, vector_schema)
    ordered_vector = encoded["encoded_vector"]

    # --- Prediction ---
    X = scaler.transform([ordered_vector])
    pred_index = model.predict(X)[0]

    probs = model.predict_proba(X)[0]
    top_sorted = sorted(enumerate(probs), key=lambda x: x[1], reverse=True)

    primary_idx, primary_prob = top_sorted[0]
    primary_label = label_map[str(primary_idx)]

    # --- Output Primary Prediction ---
    print(f"Predicted Diagnosis: **{primary_label}**")
    print(f"Confidence: {round(float(primary_prob),3)} → {confidence_label(primary_prob)}\n")

    # --- Differential Diagnosis (Top 5) ---
    print("Differential Considerations:")
    for idx, p in top_sorted[:5]:
        print(f"  • {label_map[str(idx)]}: {round(float(p),3)}")

    print("──────────────────────────────────────────\n")


# ---------------- RUN DOCTOR-STYLE TEST BANK ----------------
doctor_tests = [

    # Duchenne Muscular Dystrophy
    "3-year-old boy with delayed walking, calf pseudohypertrophy and positive Gowers sign.",
    "Progressive proximal weakness with toe walking and respiratory insufficiency.",

    # Spinal Muscular Atrophy
    "Infant with severe hypotonia, weak cry and tongue fasciculations.",
    "Floppy baby with paradoxical breathing and absent reflexes.",

    # Cystic Fibrosis
    "Recurrent pneumonia with chronic productive cough and nasal polyps.",
    "Failure to thrive with steatorrhea and digital clubbing.",

    # Marfan Syndrome
    "Tall male with long limbs, lens dislocation and pectus excavatum.",
    "Aortic root dilation with scoliosis and high arched palate.",

    # Ehlers-Danlos
    "Recurrent joint dislocations, soft stretchy skin and poor wound healing.",
    "Chronic musculoskeletal pain with joint hypermobility.",

    # Hemophilia
    "Deep muscle hematomas and prolonged bleeding after minor trauma.",
    "Recurrent hemarthrosis and bruising since childhood.",

    # Wilson’s Disease
    "Kayser-Fleischer rings with hepatic dysfunction and tremor.",
    "Behavioral changes with dystonia and chronic liver disease.",

    # Tay-Sachs Disease
    "Infant with exaggerated startle reflex, neuroregression and cherry-red spot.",
    "Loss of motor milestones with seizures and progressive paralysis.",

    # Sickle Cell Disease
    "Vaso-occlusive pain crisis with severe anemia and dactylitis.",
    "Recurrent infections with splenomegaly and leg ulcers.",

    # Thalassemia
    "Child with chronic anemia, facial bone deformities and hepatosplenomegaly.",
    "Transfusion-dependent anemia with iron overload.",

    # Phenylketonuria
    "Musty odor with developmental delay and microcephaly.",
    "Fair skin, seizures and behavioral problems in untreated PKU.",

    # Huntington's Disease
    "Adult with progressive chorea, behavioral changes and cognitive decline.",
    "Irregular involuntary movements with dysarthria and motor impersistence."
]


for t in doctor_tests:
    predict(t)
