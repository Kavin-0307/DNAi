import numpy as np
def find_symptom_index(symptom:str,text:str):
    text=text.lower()
    words=text.split()
    for i,word in enumerate(words):
        if symptom==word.strip(".,!?"):
            return i
    return None
def get_severity(symptom:str,text:str,slider_score:float|None=None)->float:
    defaultSeverity=0.5
    #it first takes into account the slider score with maximum weight
    if(slider_score!=None):
        return slider_score
    text=text.lower()
    words=text.split()
    idx=find_symptom_index(symptom,text)
    if(idx is None):
        return defaultSeverity
    window_start=max(0,idx-3)
    window_end=idx+4
    window_words=words[window_start:window_end]
    #we create a dictionary with scores of severity
    SEVERITY_SCORES={   
        "mild":0.3,
        "slight":0.3,
        "low":0.3,
        "moderate":0.6,
        "severe":0.9,
        "extreme":0.95,
        "critical":1.0,
        "very severe":1.0 
    }
    severity=None
    #we check if any severity scores are a part of the text and set it on the first go
    for word in SEVERITY_SCORES:
        if word in window_words:
            severity=SEVERITY_SCORES[word]
            break
    #we add boost words and negations if we have a severity    
    if severity is not None:
            BOOST_WORDS=["very","extremely","quite","significantly"]
            BOOST_AMOUNT=0.1
            for word in BOOST_WORDS:
                if word in window_words:
                    severity=severity+BOOST_AMOUNT
                    break
                    
            NEGATIONS=["no","not","without","denies"]
            REDUCE_AMOUNT=0.2
            symoptom_idx_in_window=idx-window_start
            for i,word in enumerate(window_words):
                if word in NEGATIONS:
                    if(i<symoptom_idx_in_window):
                        return 0.0
                    severity-=0.2
                    break
    
    else:
        severity=defaultSeverity
    if severity>1:
        severity=1
    elif severity<0:
        severity=0
 
    return severity
