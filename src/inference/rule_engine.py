import json
from pathlib import Path
#it basically applies our rules to show the updated score we think of per disease
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
#it checks if like a key symptom is available and boosts are added accordingly
def apply_pathognomic_rule(score,disease,patient_vector):
        json_path=Path(__file__).parent/"pathognomonic_map.json"
        pathognomic_map=json.loads(json_path.read_text())#importing the json
        for symptom in patient_vector:
            if symptom.startswith("_"):
                continue
            if symptom in pathognomic_map:
              if  disease==pathognomic_map[symptom]:
                 score+=0.25
                 break
        return score
#it basically applies boosts accordingly to the duration alignment
def apply_duration_alignment_rule(score,disease,patient_vector):
    json_path=Path(__file__).parent/"durations_expectations.json"
    duration_map=json.loads(json_path.read_text())#importing the json
    json_path2=Path(__file__).parent/"duration_rules.json"
    duration_rules=json.loads(json_path2.read_text())
    if disease not in duration_map:
        return score
    expected=duration_map[disease]
    durations=patient_vector.get("_duration_days",{})
    if not durations:
        return score
    durations=max(durations.values())
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


#it applies the rules basically for a disease to pass we need to calculate if it passes a minimum amount of disease

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
#cluster is basically grouping of diseases
def apply_cluster_rule(score,disease,patient_vector):
    json_path=Path(__file__).parent/"symptoms_cluster.json"
    count=0
    boost_map={
        "low":0.03,
        "medium":0.06,
        "high":0.1
    }
    symptoms_cluster_map=json.loads(json_path.read_text())#importing the json
    for cluster_name,cluster_info in symptoms_cluster_map.items():
        symptoms=cluster_info["symptoms"]
        threshold=cluster_info["trigger_threshold"]
        boost_strength=cluster_info["boost_strength"]
        match_count=sum(
            1 for symptom in symptoms
            if symptom in patient_vector and patient_vector[symptom]>0
        )
        if match_count>=threshold:
            score=score+boost_map.get(boost_strength,0.05)
    return score
def apply_confidence_rule(score,disease,patient_vector):

    confidence_dict=patient_vector.get("_confidence",{})
    if not confidence_dict:
        return score
    avg_sum=0
    count=0
    for confidence in confidence_dict.values():
        avg_sum+=confidence
        count+=1
    confidence_final=avg_sum/count
    if confidence_final>=0.85:
        score=score+0.04
    elif 0.85>confidence_final >=0.70:
        score=score+0.0
    elif 0.5<=confidence_final<0.70:
        score-=0.03
    else:
        score=score*0.8
    return score