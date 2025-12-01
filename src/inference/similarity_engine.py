from src.preprocessing.vectorization.vector_builder import get_vector
import json
import math
import numpy as np
from numpy.linalg import norm
from src.preprocessing.parsing.severity_parser import get_severity


from pathlib import Path
#this is a basic dummy implementation of our similarity, basically kinda just checks how close the input and the symptoms are it checks which disease is closely resembled in the patien
#right now the input is not taken from user needs to be CHANGED
def similarity_engine(patient_vector:dict):
   
    json_path=Path(__file__).parent/"diseases_profiles.json"
    disease_data=json.loads(json_path.read_text())#importing the json
    symptom_dict_path = Path(__file__).parent.parent/"preprocessing"/"symptom_dictionary.json"
    all_symptoms = list(json.loads(symptom_dict_path.read_text()).keys())

    scores={}#building a vector of scores based on symptom

    for disease,profile in disease_data.items():
        disease_vector=[profile.get(symptom,0) for symptom in all_symptoms]
        patient_values=[patient_vector.get(symptom,0) for symptom in all_symptoms]

        similarity=cosine_similarity(patient_values,disease_vector)
        scores[disease]=similarity
    return scores
def cosine_similarity(v1,v2):
    #should implement checks to make sure everything is not 0.TO DO
    return np.dot(v1,v2)/(norm(v1)*norm(v2))
