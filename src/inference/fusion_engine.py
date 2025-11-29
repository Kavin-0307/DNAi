from src.inference.rule_engine import apply_rules
#it calculates the probability basically by using a hybrid model both ml and hardcoding
def fusion_engine(similarity_scores:dict,patient_vector:dict):
    rules_score=apply_rules(similarity_scores,patient_vector)
    final_scores={}
    for disease in similarity_scores:
       simval=similarity_scores[disease]
       rule_score=rules_score.get(disease,simval)
       final_scores[disease]=0.6*simval+0.4*(rule_score)
    return final_scores