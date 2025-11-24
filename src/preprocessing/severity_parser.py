def get_severity(symptom:str,text:str,slider_score:float|None=None)->float:
    defaultSeverity=0.5
    if(slider_score!=None):
        return slider_score
    text=text.lower()
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
    for word in SEVERITY_SCORES:
        if word in text:
            severity=SEVERITY_SCORES[word]
            break
    if severity is not None:
            BOOST_WORDS=["very","extremely","quite","significantly"]
            BOOST_AMOUNT=0.1
            for word in BOOST_WORDS:
                if word in text:
                    severity=severity+BOOST_AMOUNT
                    break
                    
            NEGATIONS=["no","not","without","denies"]
            REDUCE_AMOUNT=0.2
            for word in NEGATIONS:
                if word in text:
                    severity=severity-REDUCE_AMOUNT
                    break
    
    else:
        severity=defaultSeverity
    if severity>1:
        severity=1
    elif severity<0:
        severity=0
    