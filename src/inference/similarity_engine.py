from src.preprocessing.vectorization.vector_builder import get_vector
import json
import math
import numpy as np
from numpy.linalg import norm
from src.training.dataset_loader import load_dataset

from src.training.feature_encoder import feature_encoder 

from src.inference.pipeline import run_pipeline 
from src.preprocessing.parsing.severity_parser import get_severity


from pathlib import Path
#this is a basic dummy implementation of our similarity, basically kinda just checks how close the input and the symptoms are it checks which disease is closely resembled in the patien
#right now the input is not taken from user needs to be CHANGED
def similarity_engine(patient_vector:list[float])->list[dict]:
   
    
    ds=load_dataset()
    X,Y=feature_encoder(ds["schema"],ds["cleaned_profiles"],ds["label_to_index"])


    results=[]#building a vector of scores based on symptom

    for index,disease_vector in enumerate(X):
        

        similarity=cosine_similarity(patient_vector,disease_vector)
        disease_name=ds["index_to_label"][index]
        results.append({disease_name:similarity})
    sorted_scores=sorted(results,key=lambda x:list(x.values())[0],reverse=True)
    return{
       "top_1":sorted_scores[0],
       "top_3":sorted_scores[3],
       "all_scores":sorted_scores
    }


def cosine_similarity(v1,v2):
    #should implement checks to make sure everything is not 0.TO DO
    if(norm(v1)==0 or norm(v2)==0):
     return 0
    return np.dot(v1,v2)/(norm(v1)*norm(v2))
    
