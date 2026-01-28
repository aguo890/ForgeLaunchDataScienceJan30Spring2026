
import nbformat as nbf
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell

nb = new_notebook()
cells = []

# Cell 1: Setup
cells.append(new_code_cell("""# notebooks/04_Risk_Watch_List.ipynb
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.abspath(os.path.join('..')))

from src.data_ingestion import load_and_clean_data
from src.features import perform_feature_engineering
from src.modeling import train_logistic_regression

# 1. Load Data (Keeping IDs)
df = load_and_clean_data(drop_id=False)
print(f"Data Loaded: {df.shape}")
print(f"Columns: {df.columns.tolist()[:5]}... (Checking for EmployeeNumber)")
"""))

# Cell 2: Modeling Prep
cells.append(new_code_cell("""# 2. Filter Active Employees (The Watch List Candidates)
# We want to score EVERYONE or just Active? Usually Watch List is for Active.
active_employees = df[df['Attrition'] == 'No'].copy()
print(f"Active Employees: {active_employees.shape[0]}")

# 3. Process Data for Modeling
# We need to process the whole dataset to train the model, 
# and also process the active employees to score them.
# Simplified: Process whole DF, then split.

df_processed = perform_feature_engineering(df)
print(f"Processed Shape: {df_processed.shape}")

# Re-identify active employees in processed data
# We assume row order is preserved (which it is)
# But safer to filter by Attrition column (which is now encoded 0/1)
# Attrition 'No' -> 0, 'Yes' -> 1
df_active_processed = df_processed[df_processed['Attrition'] == 0].copy()
df_leavers_processed = df_processed[df_processed['Attrition'] == 1].copy()

# Prepare Training Data (Full History)
X = df_processed.drop(columns=['Attrition', 'EmployeeNumber'])
y = df_processed['Attrition']

print(f"Training Features: {X.shape}")
"""))

# Cell 3: Training & Inference
cells.append(new_code_cell("""# 4. Train Winning Model (Logistic Regression)
# Note: We train on ALL history to maximize patterns.
lr_model = train_logistic_regression(X, y, class_weight='balanced')
print("Model Trained.")

# 5. Score Active Employees
# We need X for active employees only
X_active = df_active_processed.drop(columns=['Attrition', 'EmployeeNumber'])
ids_active = df_active_processed['EmployeeNumber']

# Predict Probability (Class 1 = Yes/Leave)
risk_scores = lr_model.predict_proba(X_active)[:, 1]

# Create Watch List
watch_list = pd.DataFrame({
    'EmployeeNumber': ids_active,
    'RiskScore': risk_scores
})

# Sort by Risk (Highest first)
watch_list = watch_list.sort_values(by='RiskScore', ascending=False)

# Add Risk Category
watch_list['RiskLevel'] = pd.cut(watch_list['RiskScore'], 
                                 bins=[0, 0.3, 0.7, 1.0], 
                                 labels=['Low', 'Medium', 'High'])

print("Top 10 At-Risk Employees:")
print(watch_list.head(10))
"""))

# Cell 4: Export
cells.append(new_code_cell("""# 6. Export
output_dir = Path('../results')
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / 'risk_watch_list.csv'

watch_list.to_csv(output_path, index=False)
print(f"Watch List saved to: {output_path}")
"""))

nb['cells'] = cells

with open('notebooks/04_Risk_Watch_List.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Created notebooks/04_Risk_Watch_List.ipynb")
