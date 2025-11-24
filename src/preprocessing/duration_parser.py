import re
def get_duration_days(symptom:str,text:str)->int:
    data=re.search('(\d+)\s+(day|day|week|weeks|month|months|year|years)',text)
    #if data is empty assume 3 days
    if data is None:
        return 3
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
    #return whatever the duration in terms of days
    amt=int(data.group(1))
    unit=data.group(2)
    days=amt*multiplier_dict[unit]
    return days

   
    