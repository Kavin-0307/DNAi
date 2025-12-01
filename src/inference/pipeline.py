#Normalization
from src.preprocessing.normalization.attribute_normalizer import normalize_attributes_text
from src.preprocessing.normalization.cue_normalizer import normalize_cues
from src.preprocessing.normalization.concept_normalizer import normalize_concepts

# Parsing
from src.preprocessing.parsing.duration_parser import get_duration_days
from src.preprocessing.parsing.severity_parser import get_severity
from src.preprocessing.parsing.negation_detector import NegationDetector
from src.preprocessing.parsing.uncertainity_detector import UncertaintyDetector

#Vectorization
from src.preprocessing.vectorization.vector_builder import get_vector

import json
import re
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYMPTOM_FILE = os.path.join(BASE_DIR, "..", "preprocessing", "vectorization", "symptom_dictionary.json")
SYMPTOM_FILE = os.path.normpath(SYMPTOM_FILE)


def extract_symptoms(text:str)-> list:
    #This is a diagnosis inference pipeline that takes input as raw text and outputs structured inference
    
    with open(SYMPTOM_FILE,'r') as f:
        dictionary=json.load(f)
    detected=[]
    
    for canonical,synonyms in dictionary.items():
        for word in synonyms:
            pattern=rf"\b{re.escape(word.lower())}\b"
            if re.search(pattern,text.lower()):
                detected.append(canonical)
    return list(set(detected))
def run_pipeline(text:str)->dict:
    symptoms=extract_symptoms(text)
    if not symptoms:
        return{"error":"No symptoms detected","normalized_text":text}
    
    negation_detector=NegationDetector()
    uncertainty_detector=UncertaintyDetector()

    negation_map=negation_detector.detect(text,symptoms)
    uncertainty_map=uncertainty_detector.detect(text,symptoms)

    structured={}
    for s in symptoms:
        structured[s]={
            "duration_days":get_duration_days(text,s),
            "severity":get_severity(s,text),
            "negated":negation_map.get(s,False),
            "uncertain":uncertainty_map.get(s,False)
        }   
    structured = normalize_concepts(structured)
    SCHEMA_FILE = os.path.join(BASE_DIR, "..","..", "models", "vector_schema.json")
    SCHEMA_FILE = os.path.normpath(SCHEMA_FILE)

    with open(SCHEMA_FILE,"r") as f:
            schema=json.load(f)
    encoded=get_vector(structured,schema)

    return{
       "normalized_text": text,
        "symptoms": structured,
        "encoded_vector": encoded["encoded_vector"],
        "symptom_order": encoded["symptom_order"],

    }