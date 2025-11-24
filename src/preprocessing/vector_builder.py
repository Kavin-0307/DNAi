from severity_parser import get_severity
from duration_parser import get_duration_days
def vector_builder(symptom_prescence:dict,text:str)->dict:
    vector={}
    vector["_duration_days"]={}
    #loops over symptoms found in text
    for symptom in symptom_prescence:
        if symptom_prescence[symptom]==True:
            #if symptom is found we compute severity+duration
            severity=get_severity( symptom,text)#calls the get severity function
            duration=get_duration_days(symptom,text)
            vector[symptom]=severity#store numeric severity score for symptom
            vector["_duration_days"][symptom]=duration#store number of days for a certain symptom
        else:
            severity=0.0
            vector[symptom]=severity
    return vector                
    
          