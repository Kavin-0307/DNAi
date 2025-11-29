import re
from src.preprocessing.severity_parser import find_symptom_index
def get_duration_days(symptom:str,text:str)->int:
   # we first split the entire incoming text into words
    words=text.lower().split()
    #find the index of the symptoms in the text
    idx=find_symptom_index(symptom,text)
    if idx is None:
        return None#if not found return Null value
    search_words=words[idx:idx+8]#checking to see basically if there is any multiplier within a set span of the symptom
    joined=" ".join(search_words)
    data=re.search(r"(\d+)\s+(day|days|week|weeks|month|months|year|years)",joined)#regex to parse input
     #if data is empty null return
    if data is None:
        return None
    #the next part is the multiplier dictionary, the current version is rudimentary but i would add more stuff into it later on 
    multiplier_dict={
        "weeks":7,
        "years":365,
        "months":30,
        "days":1,
        "week":7,
        "year":365,
        "month":30,
        "day":1
    
    }
    
    number=int(data.group(1))
    amt=data.group(2)
    return number*multiplier_dict[amt]
    

   
    