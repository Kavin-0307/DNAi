from src.inference.rule_engine import apply_rules
def fusion_engine(similarity_scores:dict,patient_vector:dict):
    rules_score=apply_rules(similarity_scores,patient_vector)
    final_scores={}
    for disease in similarity_scores:
       simval=similarity_scores[disease]
       rule_score=rules_score.get(disease,simval)
       final_scores[disease]=0.6*similarity_scores[disease]+0.4*(rules_score[disease])
    return final_scores