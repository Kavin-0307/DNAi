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
    json_path2=Path(__file__).parent/"durations_rules.json"
    duration_rules=json.loads(json_path2.read_text())
    if disease not in duration_map:
        return score
    expected=duration_map[disease]
    durations=max(patient_vector["_duration_days"].values())
    if durations>0 and durations<=7:
        severity="acute"
    elif durations>7 and durations<=60:
        severity="subacute"
    elif durations>=60:
        severity="chronic"
    action=duration_rules.get(expected,{}).get(severity)
    if not action:
        return score
    if action.startswith("*"):
        score*=float(action[1:])
    else:
        score+=float(action)
    return score



def apply_required_symptoms_rule(score,disease,patient_vector):
    json_path=Path(__file__).parent/"required_symptoms.json"
    required_symptoms_map=json.loads(json_path.read_text())#importing the json
    strict_required = ["duchenne_muscular_dystrophy",
                   "spinal_muscular_atrophy",
                   "tay_sachs_disease"]
    

    if disease not in required_symptoms_map:
        return score
    required_list=required_symptoms_map[disease]
    c=0
    for symptom in required_list:
        if symptom in patient_vector and patient_vector[symptom]>0:
            c+=1
    total_required=len(required_list)
    ratio=c/total_required    
    if disease in strict_required:
        if ratio==0:
            score=0.05
        elif ratio<1:
            score*=0.5
        else:
            score+=0.05
    else:
        if ratio<0.25:
            score-=0.10
        elif ratio>=0.75:
            score+=0.05
        
    return score
def apply_cluster_rule(score,disease,patient_vector):
    json_path=Path(__file__).parent/"symptoms_cluster.json"
    symptoms_cluster_map=json.loads(json_path.read_text())#importing the json
    
    return score
def apply_confidence_rule(score,disease,patient_vector):
    json_path=Path(__file__).parent/"duration_expectations.json"
    confidence_map=json.loads(json_path.read_text())#importing the json
    return score