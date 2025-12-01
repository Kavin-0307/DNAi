import os
from pathlib import Path
import numpy as np
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent.parent  
SCALER_PATH = BASE_DIR / "models" / "scalers" / "standard_scaler.joblib"


_scaler = None

def _load_scaler():
    global _scaler
    if _scaler is None:
        if not SCALER_PATH.exists():
            print("Scaler not found ")
            return None

        _scaler = joblib.load(SCALER_PATH)
        print(f"[scaling] Scaler loaded from: {SCALER_PATH}")

    return _scaler

def scale_vector(vector):
  
    scaler = _load_scaler()

    if scaler is None:
        return np.array(vector)

    vector = np.array(vector).reshape(1, -1)
    scaled = scaler.transform(vector)
    return scaled.flatten()
