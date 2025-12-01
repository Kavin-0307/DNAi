from src.preprocessing.parsing.duration_parser import get_duration_days
from src.preprocessing.parsing.severity_parser import get_severity
import json
def get_vector(structured_symptoms:dict,schema:dict)->dict:

    
    
    base_conf=0.7
    #loops over symptoms found in text
    presence_block=[]
    severity_block=[]
    duration_block=[]
    certainty_block=[]
    for symptom in schema["symptom_order"]:
        data = structured_symptoms.get(symptom,None)
        confidence=base_conf
        if data is not None and data["negated"]==False:
            #if symptom is found we compute severity+duration
            presence = 1
            severity = data["severity"]
            duration = data["duration_days"]
            confidence=confidence+0.2#small boost for postive match
        elif  data and data["negated"] is True :
                    presence=0
                    severity=0
                    duration=0
                
        else:
                
                    presence=-1
                    severity=0
                    duration=0
                    certainty_block.append(-1)
                    presence_block.append(presence)
                    severity_block.append(severity)
                    duration_block.append(duration)
                    
                    continue
       
               
        if data and data["duration_days"]>0:
            confidence+=0.1
        confidence=max(0,min(1,confidence))#clamp values
        presence_block.append(presence)
        severity_block.append(severity)
        duration_block.append(duration)
        certainty_block.append(confidence)
        

    return {
        "encoded_vector": presence_block + severity_block + duration_block + certainty_block,
        "symptom_order": schema["symptom_order"]
    }