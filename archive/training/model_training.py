import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
import joblib
data=pd.read_csv('data/processed/diabetes_cleaned.csv')
X=data.drop('Outcome',axis=1)
y=data['Outcome']

#random state hear refers to randomness for reproducibility of results
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
scaler=StandardScaler()
#scaling is the process of transforming the data into a common range,like 0 to 1
X_train_scaled=scaler.fit_transform(X_train)
X_test_scaled=scaler.transform(X_test)
#i applied logistic regresssion to our scaled training data , tested its predictions 
log_reg=LogisticRegression(solver='liblinear',random_state=42,max_iter=1000)
log_reg.fit(X_train_scaled,y_train)
predictions=log_reg.predict(X_test_scaled)
probabilities=log_reg.predict_proba(X_test_scaled)
#the classification report
report=classification_report(y_test,predictions)
#Confusion matrix
cm=confusion_matrix(y_test,predictions)
#accuracy
accuracy=accuracy_score(y_test,predictions)
#roc_auc_score
auc_score=roc_auc_score(y_test,probabilities[:,1])
#roc curve
flpr,tpr,thresholds=roc_curve(y_test,probabilities[:,1])
print(report)
print("Accuracy:",accuracy)
print("AUC:",auc_score)
print("\n")
print("confusion matrix",cm)

joblib.dump(log_reg, "models/log_reg.joblib")

joblib.dump(scaler, "models/scalers/standard_scaler.joblib")
print("model saved ")