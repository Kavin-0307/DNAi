import numpy as np
def feature_encoder(schema:dict,cleaned_profiles:dict,label_to_index:dict):
    final_vec=[]
    labels=[]
    for disease in cleaned_profiles:
        vec=[]
        for symptom in schema["symptom_order"]:
            if symptom in cleaned_profiles[disease]:
                vec.append(1)
            else:
                vec.append(0)
        final_vec.append(vec)
        labels.append(label_to_index[disease])
    X=np.array(final_vec)
    Y=np.array(labels)
    return X,Y
            