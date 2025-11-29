# explanation_engine.py
#so what it does is it basically takes all the input our other files generate and turns into in human explanation.
#right now it is hardcoded but the final aim is to not be.I dont know how yet
def explanation_engine(disease:str,patient_vector:dict,similarity_scores:dict,rule_log:dict)->dict:
    explanation=[] 
    #we get the similarity score to the final disease from the dictionary,falls back to default
    sim_score = similarity_scores.get(disease,0)
    explanation.append(f"Similarity match score: {sim_score:.2f}")
    #so now it checks if key symptom is found that differentiates a disease.If so it appends to the explanation vector
    if rule_log.get("pathognomonic_hit"):
        explanation.append(f"Detected key diagnostic symptom: {rule_log['pathognomonic_hit']} (strong indicator)")
    #the clusters get triggered if there is a hit and then we append it to this explanation 
    if rule_log.get("clusters_triggered"):
        clusters=", ".join(rule_log["clusters_triggered"])
        explanation.append(f"Symptom cluster triggered: {clusters}")
    #this basically checks how many of the actual symptoms match for a disease.
    if "required_ratio" in rule_log:
        ratio=rule_log["required_ratio"]*100
        explanation.append(f"Required symptoms matched: {ratio:.0f}%")
    #basically how the disease behaves vs how you are based on symptom history
    if rule_log.get("duration_match"):
        explanation.append(f"Symptom duration aligns with expected pattern: {rule_log['duration_match']}")
    #gets confidence from the confidence sub dictionary in the patient_vector
    conf_dict=patient_vector.get("_confidence",{})
    if conf_dict:
        avg=sum(conf_dict.values())/len(conf_dict)
        explanation.append(f"Extraction confidence: {avg:.2f}")
    #builds the final string 
    formatted="\n".join(["- "+item for item in explanation])

    result={
        "diagnosis":disease,
        "explanation_points":explanation,
        "formatted_output":f"Reasoning for {disease}:\n\n{formatted}"
    }

    return result
