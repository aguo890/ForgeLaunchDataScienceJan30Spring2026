
import nbformat as nbf
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell

nb = new_notebook()
cells = []

# Cell 1: Setup
cells.append(new_code_cell("""# notebooks/03_Modeling.ipynb
import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join('..')))

from src.modeling import (load_processed_data, apply_smote, train_logistic_regression, 
                          train_xgboost, evaluate_model, get_shap_values)

# Visual settings
plt.rcParams["figure.figsize"] = (10, 6)
"""))

# Cell 2: Load Data
cells.append(new_code_cell("""# 1. Load Processed Data
X_train, y_train, X_test, y_test = load_processed_data('../data/processed')
print(f"Train Shape: {X_train.shape}, Test Shape: {X_test.shape}")
print(f"Train Class Distribution:\\n{y_train.value_counts(normalize=True)}")
"""))

# Cell 3: Baseline Logistic Regression
cells.append(new_code_cell("""# 2. Baseline: Logistic Regression (Class Weight Balanced)
lr_model = train_logistic_regression(X_train, y_train, class_weight='balanced')
evaluate_model(lr_model, X_test, y_test, model_name="Logistic Regression")
"""))

# Cell 4: SMOTE
cells.append(new_code_cell("""# 3. Handling Imbalance: SMOTE
X_train_smote, y_train_smote = apply_smote(X_train, y_train)
print(f"Shape after SMOTE: {X_train_smote.shape}")
print(f"Class Distribution after SMOTE:\\n{y_train_smote.value_counts(normalize=True)}")
"""))

# Cell 5: XGBoost
cells.append(new_code_cell("""# 4. Advanced Model: XGBoost on SMOTE Data
xgb_model = train_xgboost(X_train_smote, y_train_smote)
evaluate_model(xgb_model, X_test, y_test, model_name="XGBoost (with SMOTE)")
"""))

# Cell 6: SHAP Visualization
cells.append(new_code_cell("""# 5. Interpretation: SHAP Values
# We explain the XGBoost model using the Test set (or a sample of it)
explainer, shap_values = get_shap_values(xgb_model, X_test)

# Summary Plot
plt.figure()
shap.summary_plot(shap_values, X_test, show=False)
plt.title("SHAP Summary Plot - Feature Importance & Direction", fontsize=14)
plt.tight_layout()
plt.show()

# Validating the "OverTime" hypothesis
try:
    if 'OverTime_1' in X_test.columns: # If One-Hot encoded, it might be OverTime_1 or OverTime_Yes
        print("Checking OverTime feature importance...")
    else:
        # Check columns
        print("Columns:", X_test.columns.tolist())
except Exception as e:
    print(e)
"""))

nb['cells'] = cells

with open('notebooks/03_Modeling.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Created notebooks/03_Modeling.ipynb")
