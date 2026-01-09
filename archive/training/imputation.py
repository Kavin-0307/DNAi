import numpy as np
import pandas as pd
from pathlib import Path
RAW_FILE = Path("data/raw/diabetes.csv")
OUTPUT_FILE = Path("data/processed/diabetes_cleaned.csv")


data=pd.read_csv('data/raw/diabetes.csv')
#basically loads only those columns we need
columns_to_impute=['Glucose','BloodPressure','SkinThickness','Insulin','BMI']
#it sets 0 to nan, makes life easier for later on
data[columns_to_impute]=data[columns_to_impute].replace(0,np.nan)
#calulates the median of the columns to set
imputation_values=data[columns_to_impute].median()
data.fillna(imputation_values,inplace=True)
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
data.to_csv(OUTPUT_FILE, index=False)


data.to_csv('data/processed/diabetes_cleaned.csv', index=False)
