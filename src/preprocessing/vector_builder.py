from src.preprocessing.duration_parser import get_duration_days
from src.preprocessing.severity_parser import get_severity

def get_vector(symptom_prescence:dict,text:str)->dict:
    vector={}
    vector["_duration_days"]={}
    vector["_confidence"]={}
    base_conf=0.7
    #loops over symptoms found in text
    for symptom in symptom_prescence:
        if symptom_prescence[symptom]==True:
            #if symptom is found we compute severity+duration
            severity=get_severity( symptom,text)#calls the get severity function
            confidence=base_conf+0.2#small boost for postive match
        else:
            severity=0.0
            confidence=base_conf
        duration=get_duration_days(symptom,text)
        if duration and duration>0:
            confidence+=0.1
        confidence=max(0,min(1,confidence))#clamp values
        vector[symptom]=severity#store numeric severity score for symptom
        vector["_duration_days"][symptom]=duration#store number of days for a certain symptom
        vector["_confidence"][symptom]=confidence
    return vector                
    
          