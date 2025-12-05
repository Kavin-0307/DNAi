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
from difflib import SequenceMatcher
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYMPTOM_FILE = os.path.join(BASE_DIR, "..", "preprocessing", "vectorization", "symptom_dictionary.json")
SYMPTOM_FILE = os.path.normpath(SYMPTOM_FILE)


def extract_symptoms(text:str)-> list:
    #This is a diagnosis inference pipeline that takes input as raw text and outputs structured inference
    
    with open(SYMPTOM_FILE,'r') as f:
        dictionary=json.load(f)
    detected=[]
    text_lower=text.lower()
    text_clean = re.sub(r'[^a-z0-9 ]', ' ', text.lower()).strip()
    text_words = text_clean.split()
    for canonical,synonyms in dictionary.items():
      for synonym in synonyms:
        syn_clean=re.sub(r'[^a-z0-9 ]', ' ',synonym.lower()).strip()
        syn_token=syn_clean.split()
        if syn_clean and re.search(rf"\b{syn_clean}\b", text_clean):
                if contextual_validation(canonical,text_clean):
                        detected.append(canonical)
                    
                        break

        if len(syn_token)>1:
              for i in range(len(text_words) -  len(syn_token)+ 1):
                chunk = " ".join(text_words[i:i+ len(syn_token)])
                if similarity(syn_clean, chunk) >=0.65:
                 if contextual_validation(canonical,text_clean):
                        detected.append(canonical)
                    
                        break
        else :
            syn=syn_token[0]
            for w in text_words:
               
                if len(w)>4 and similarity(w,syn) >=0.55:
                    if contextual_validation(canonical,text_clean):
                        detected.append(canonical)
                    
                        break

          
                


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
def similarity(a,b):
    return SequenceMatcher(None,a.lower(),b.lower()).ratio()
def contextual_validation(symptom, text):
    context_keywords = {
        "waddling_gait": ["walk", "gait", "movement"],
        "gowers_sign": ["stand", "rise", "weakness"],
        "nasal_polyps": ["nose", "sinus", "breathing"],
        "vaso_occlusive_crisis": ["pain", "crisis", "swelling"],
        "kayser_fleischer_rings": ["eye", "copper", "brown ring"],
        "scoliosis": ["spine", "back", "curve"],
        "toe_walking": ["walk", "gait", "balance"],
        "pseudohypertrophy": ["calf", "muscle"]
    }
    if symptom not in context_keywords:
        return True
    for word in context_keywords.get(symptom, []):
        if word in text:
            return True
    return False
