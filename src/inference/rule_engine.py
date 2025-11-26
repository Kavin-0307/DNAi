import json
from pathlib import Path

def apply_rules(similarity_scores:dict,patient_vector:dict)->dict:
    updated_scores={}
    for disease,score in similarity_scores.items():
        modified=score
        modified=apply_pathognomic_rule(modified,disease,patient_vector)
        modified=apply_required_symptoms_rule(modified,disease,patient_vector)
        modified=apply_duration_alignment_rule(modified,disease,patient_vector)
        modified=apply_cluster_rule(modified,disease,patient_vector)
        modified=apply_confidence_rule(modified,disease,patient_vector)
        updated_scores[disease]=modified
    return updated_scores
def apply_pathognomic_rule(score,disease,patient_vector):
        json_path=Path(__file__).parent/"pathognomonic_map.json"
        pathognomic_map=json.loads(json_path.read_text())#importing the json
        for symptom in patient_vector:
            if symptom in pathognomic_map:
              if  disease==pathognomic_map[symptom]:
                 score+=0.25
                 break
        return score

def apply_duration_alignment_rule(score,disease,patient_vector):
    json_path=Path(__file__).parent/"durations_expectations.json"
    duration_map=json.loads(json_path.read_text())#importing the json
    
   
    return score
def apply_required_symptoms_rule(score,disease,patient_vector):
    json_path=Path(__file__).parent/"required_symptoms.json"
    required_symptoms_map=json.loads(json_path.read_text())#importing the json
    for symptom in patient_vector:
        if symptom:
            ""
    return score
def apply_cluster_rule(score,disease,patient_vector):
    json_path=Path(__file__).parent/"symptoms_cluster.json"
    symptoms_cluster_map=json.loads(json_path.read_text())#importing the json
    return score
def apply_confidence_rule(score,disease,patient_vector):
    json_path=Path(__file__).parent/"duration_expectations.json"
    confidence_map=json.loads(json_path.read_text())#importing the json
    return score