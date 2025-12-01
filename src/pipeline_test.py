# src/pipeline_test.py

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.inference.pipeline import run_pipeline

text = "I have severe chest pain and mild fever for 3 days, but I’m not sure."
result = run_pipeline(text)

print(result)
