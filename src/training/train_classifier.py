import numpy as np
import pandas as pd
import json 
import joblib
from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression 
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from src.training.dataset_builder import dataset_builder
X_dataset,Y_dataset=dataset_builder()
print(f"\nDataset Ready: {len(X_dataset)} samples | {len(set(Y_dataset))} diseases")
label_encoder = LabelEncoder()
Y_dataset = label_encoder.fit_transform(Y_dataset)
X_train,X_test,Y_train,Y_test=train_test_split(X_dataset,Y_dataset,stratify=Y_dataset,test_size=0.2,random_state=42)
scaler=StandardScaler()
X_train_scaled=scaler.fit_transform(X_train)
X_test_scaled=scaler.transform(X_test)

log_reg=LogisticRegression(solver="liblinear",random_state=42,max_iter=2000,class_weight="balanced")
log_reg.fit(X_train_scaled,Y_train)
prediction=log_reg.predict(X_test_scaled)
probabilities=log_reg.predict_proba(X_test_scaled)

report=classification_report(Y_test,prediction)
accuracy=accuracy_score(Y_test,prediction)
cm=confusion_matrix(Y_test,prediction)
print("Accuracy:",accuracy)
print("confusion matrix",cm)

joblib.dump(log_reg, "models/symptom_classifier.pkl")

joblib.dump(scaler, "models/scalers/standard_scaler.joblib")
label_map = {int(i): label for i, label in enumerate(label_encoder.classes_)}
with open("models/label_map.json", "w") as f:
    json.dump(label_map, f, indent=2)
print("model saved ")