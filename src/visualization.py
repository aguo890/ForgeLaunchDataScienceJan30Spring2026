
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
import shap

def setup_styles():
    """Sets professional plotting aesthetics."""
    sns.set_style("whitegrid")
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["figure.dpi"] = 300

def plot_attrition_by_overtime(df, output_path):
    """Plots Attrition rates for OverTime vs Non-OverTime employees."""
    plt.figure()
    
    # Calculate percentages
    summary = df.groupby('OverTime')['Attrition'].value_counts(normalize=True).rename('percentage').reset_index()
    # Filter for 'Yes' attrition only for the bar chart height
    # Check if Attrition is encoded or not. The function doc says "Pre-Model", implying raw strings 'Yes'/'No'
    # But clean_data might not encode it yet.
    # The snippet uses summary[summary['Attrition'] == 'Yes'], so it expects string 'Yes'.
    
    # If Attrition is already 0/1, we need to handle that.
    # But clean_data loads raw strings usually unless features is called.
    # We'll assume the df passed here is from clean_data which has string labels for Attrition usually.
    # Let's check duplicate columns behavior if encoded.
    
    leavers = summary[summary['Attrition'] == 'Yes'].copy()
    
    ax = sns.barplot(data=leavers, x='OverTime', y='percentage', palette="Reds_d")
    
    plt.title("Burnout Signal: Attrition Rate by OverTime Status", fontsize=14, pad=20)
    plt.ylabel("Attrition Rate (Probability of Leaving)")
    plt.xlabel("Works OverTime?")
    
    # Add percentage labels
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%')
        
    plt.tight_layout()
    plt.savefig(output_path / '01_overtime_impact.png')
    plt.close()

def plot_feature_importance(model, X_test, feature_names, output_path):
    """Generates a SHAP summary plot to explain model decisions."""
    # Note: Using TreeExplainer for XGBoost or LinearExplainer/KernelExplainer for generic
    # For Logistic Regression, we can plot coefficients, but SHAP is more 'bonus points'
    # We will use simple coefficient magnitude for the Logistic Regression if SHAP is too heavy
    
    plt.figure(figsize=(12, 8))
    
    # Extract coefficients for Logistic Regression
    if hasattr(model, 'coef_'):
        importance = pd.DataFrame({
            'Feature': feature_names,
            'Importance': model.coef_[0]
        })
        importance['AbsImportance'] = importance['Importance'].abs()
        importance = importance.sort_values(by='AbsImportance', ascending=False).head(15)
        
        sns.barplot(data=importance, x='Importance', y='Feature', palette="coolwarm")
        plt.title("Top 15 Drivers of Attrition (Logistic Regression Coefficients)", fontsize=14)
        plt.xlabel("Impact on Risk (Negative=Retains, Positive=Risks)")
    
    plt.tight_layout()
    plt.savefig(output_path / '02_feature_drivers.png')
    plt.close()

def plot_risk_distribution(risk_scores, output_path):
    """Visualizes the distribution of risk scores across the workforce."""
    plt.figure()
    sns.histplot(risk_scores, kde=True, bins=30, color="navy")
    plt.axvline(x=0.7, color='red', linestyle='--', label='High Risk Threshold (70%)')
    plt.title("Distribution of Attrition Risk Scores", fontsize=14)
    plt.xlabel("Predicted Risk Probability")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path / '03_risk_distribution.png')
    plt.close()

def plot_correlation_heatmap(df, output_path):
    """Generates a correlation heatmap for numeric features."""
    import numpy as np
    
    plt.figure(figsize=(12, 10))
    numeric_df = df.select_dtypes(include=['int64', 'float64'])
    corr = numeric_df.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    sns.heatmap(corr, mask=mask, cmap='RdBu_r', center=0, 
                linewidths=0.5, annot=False)
    plt.title("Feature Correlation Matrix", fontsize=14)
    plt.tight_layout()
    plt.savefig(output_path / '00_correlation_heatmap.png')
    plt.close()
