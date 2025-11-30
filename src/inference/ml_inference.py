import joblib
import numpy as np
scaler=joblib.load('models/scalers/standard_scaler.joblib')
model=joblib.load('models/log_reg.joblib')
Feature_Order = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age"
]

def predict_diabetes(patient_vector:dict)->dict:
    features_list=[]
    for feature in Feature_Order:
        features_list.append(patient_vector.get(feature,0))
    feature_array=np.array(features_list).reshape(1,-1)
    array_scaled=scaler.transform(feature_array)

    prediction=model.predict(array_scaled)[0]
    probability=model.predict_proba(array_scaled)[0][1]

    return{
        "prediction":(int)(prediction),
        "probability":float(round(probability,4))
    }
    
   

