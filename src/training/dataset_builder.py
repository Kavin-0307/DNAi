import json
from pathlib import Path
from src.inference.pipeline import run_pipeline
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CASES_FILE = PROJECT_ROOT / "data" / "synthetic" / "n1_training_cases.json"

def dataset_builder(file_path=None):
    if file_path is None:
        file_path = CASES_FILE   

    with open(file_path,'r') as f:
        clinical_cases=json.load(f)
    
    X_dataset=[]
    Y_dataset=[]

    for idx,case in enumerate(clinical_cases):
        disease_label=case["disease"]
        text=case["text"]
        structured=run_pipeline(text)
        if "encoded_vector" not in structured:
            print("Not Exist")
            continue
        vector=structured["encoded_vector"]
        if not vector:
            print("empty vector")
            continue
        X_dataset.append(vector)
        Y_dataset.append(disease_label)
    return X_dataset,Y_dataset