
import nbformat as nbf
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell

nb = new_notebook()
cells = []

# Cell 1: Setup
cells.append(new_code_cell("""# notebooks/02_Feature_Engineering.ipynb
import pandas as pd
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.abspath(os.path.join('..')))

from src.data_ingestion import load_and_clean_data
from src.features import perform_feature_engineering, split_data
"""))

# Cell 2: Execution
cells.append(new_code_cell("""# 1. Load Data
df = load_and_clean_data()
print(f"Data Loaded: {df.shape}")

# 2. Feature Engineering Pipeline
# (Construction, Encoding, Scaling)
df_processed = perform_feature_engineering(df)
print(f"Data Processed: {df_processed.shape}")
print("New Features check:")
print(df_processed[['TenureRatio', 'PromotionStagnation', 'IncomeStability', 'SatisfactionComposite']].head())

# 3. Stratified Split
X_train, X_test, y_train, y_test = split_data(df_processed, target_col='Attrition')
print(f"Train Scaled Shape: {X_train.shape}")
print(f"Test Scaled Shape: {X_test.shape}")
print(f"Train Attrition Rate: {y_train.mean():.1%}")
print(f"Test Attrition Rate: {y_test.mean():.1%}")

# 4. Save to Processed
output_dir = Path('../data/processed')
output_dir.mkdir(parents=True, exist_ok=True)

# Save as Parquet (preserving schema)
# We need to recombine X and y for saving, or save separately.
# Let's save separately to avoid re-splitting issues.

X_train.join(y_train).to_parquet(output_dir / 'train.parquet', index=False)
X_test.join(y_test).to_parquet(output_dir / 'test.parquet', index=False)

print("Saved train.parquet and test.parquet to data/processed/")
"""))

nb['cells'] = cells

with open('notebooks/02_Feature_Engineering.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Created notebooks/02_Feature_Engineering.ipynb")
