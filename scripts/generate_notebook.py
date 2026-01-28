
import nbformat as nbf
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell

nb = new_notebook()

cells = []

# Cell 1: Imports and Setup
cells.append(new_code_cell("""# notebooks/01_EDA.ipynb

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os

# Add 'src' to path to import modules
sys.path.append(os.path.abspath(os.path.join('..')))

from src.data_ingestion import load_and_clean_data

# Set visual style
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)"""))

# Cell 2: Load Data
cells.append(new_code_cell("""# 1. Load Data
try:
    df = load_and_clean_data()
    print(f"Data Loaded Successfully: {df.shape}")
except FileNotFoundError as e:
    print(e)"""))

# Cell 3: Hypothesis 1
cells.append(new_code_cell("""# 2. Hypothesis 1: The "Burnout" Factor (OverTime)
plt.figure()
ax = sns.countplot(x='OverTime', hue='Attrition', data=df, palette='viridis')
plt.title('Attrition Distribution by OverTime Status', fontsize=14)
plt.ylabel('Count')

# Calculate percentages for annotation
total = len(df)
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x() + p.get_width() / 2., height + 5,
            '{:1.1f}%'.format(100 * height / total),
            ha="center") 
plt.show()

# Insight Calculation
ot_attrition = df[df['OverTime'] == 'Yes']['Attrition'].value_counts(normalize=True)
print(f"Attrition Rate for OverTime Employees: {ot_attrition['Yes']:.1%}")"""))

# Cell 4: Hypothesis 2
cells.append(new_code_cell("""# 3. Hypothesis 2: The "Compensation" Factor
plt.figure()
sns.boxplot(x='Attrition', y='MonthlyIncome', data=df, palette='coolwarm')
plt.title('Monthly Income Distribution: Leavers vs. Stayers', fontsize=14)
plt.show()"""))

# Cell 5: Hypothesis 3
cells.append(new_code_cell("""# 4. Hypothesis 3: The "Sales" Cohort Risk
plt.figure(figsize=(12, 6))
# Calculate attrition rates by role
attrition_by_role = df.groupby('JobRole')['Attrition'].apply(lambda x: (x == 'Yes').sum() / len(x)).reset_index(name='AttritionRate')
attrition_by_role = attrition_by_role.sort_values(by='AttritionRate', ascending=False)

sns.barplot(x='AttritionRate', y='JobRole', data=attrition_by_role, palette='Reds_r')
plt.title('Attrition Rate by Job Role', fontsize=14)
plt.xlabel('Attrition Rate (0.0 - 1.0)')
plt.axvline(x=0.16, color='k', linestyle='--', label='Average Attrition (16%)') # Benchmark line
plt.legend()
plt.show()

# Insight Calculation
print("Attrition by Job Role:")
print(attrition_by_role)"""))

# Cell 6: Correlation
cells.append(new_code_cell("""# 5. Correlation Heatmap (Multivariate)
# numeric_only=True is required for newer pandas versions
plt.figure(figsize=(12, 10))
numeric_df = df.select_dtypes(include=['int64', 'float64'])
corr = numeric_df.corr()
mask =  np.triu(np.ones_like(corr, dtype=bool)) # Mask upper triangle
sns.heatmap(corr, mask=mask, cmap='RdBu_r', center=0, linewidths=0.5, annot=False)
plt.title('Feature Correlation Matrix', fontsize=14)
plt.show()"""))

nb['cells'] = cells

with open('notebooks/01_EDA.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Created notebooks/01_EDA.ipynb")
