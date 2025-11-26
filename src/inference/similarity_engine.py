from src.preprocessing.vector_builder import get_vector
import json
import math
import numpy as np
from numpy.linalg import norm
from src.preprocessing.severity_parser import get_severity
from pathlib import Path
#this is a basic dummy implementation of our similarity, basically kinda just checks how close the input and the symptoms are it checks which disease is closely resembled in the patien
#right now the input is not taken from user needs to be CHANGED
def similarity_engine():
    dummy_text = "Patient reports cough and chest pain for 5 days"#Mock input to test
    dummy_symptoms = {"cough": True, "chest pain": True, "fever": False}#mock input to be removed
    patient_data=get_vector(dummy_symptoms,dummy_text)
    json_path=Path(__file__).parent/"diseases_profiles.json"
    disease_data=json.loads(json_path.read_text())#importing the json
    all_symptoms=sorted(disease_data[next(iter(disease_data))].keys())
    scores={}#building a vector of scores based on symptom

    for disease,profile in disease_data.items():
        disease_vector=[profile.get(symptom,0) for symptom in all_symptoms]
        patient_vector=[patient_data.get(symptom,0) for symptom in all_symptoms]

        similarity=cosine_similarity(patient_vector,disease_vector)
        scores[disease]=similarity
    return scores
def cosine_similarity(v1,v2):
    #should implement checks to make sure everything is not 0.TO DO
    return np.dot(v1,v2)/(norm(v1)*norm(v2))
    
if __name__=="__main__":
   print( similarity_engine())