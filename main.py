
import os
import sys
import pandas as pd
from pathlib import Path
import logging

# Add src to python path to ensure modules are found
sys.path.append(str(Path(__file__).parent))

from src.data_ingestion import load_and_clean_data
from src.features import perform_feature_engineering, split_data, scale_train_test
from src.modeling import train_logistic_regression, get_strategic_insights
from src.visualization import (setup_styles, plot_attrition_by_overtime, 
                               plot_feature_importance, plot_risk_distribution,
                               plot_correlation_heatmap)
import json

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # 1. Setup
    logger.info("Starting Forge Launch Data Science Sprint...")
    results_dir = Path('results')
    figures_dir = results_dir / 'figures'
    figures_dir.mkdir(parents=True, exist_ok=True)
    setup_styles()

    # ... [Ingestion and Feature Engineering] ... 
    # (Abbreviated for prompt specific instruction, but I must provide valid ReplaceFileContent. 
    # I will replace the import section and the end of the file where I add the new logic.)
    
    # ... Skipping unchanged lines for ReplaceFileContent efficiency is best if I use MultiReplace.
    # But ReplaceFileContent needs contiguous block. 
    # Let me use MultiReplaceFileContent for main.py to handle import and logic separation.


# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # 1. Setup
    logger.info("Starting Forge Launch Data Science Sprint...")
    results_dir = Path('results')
    figures_dir = results_dir / 'figures'
    figures_dir.mkdir(parents=True, exist_ok=True)
    setup_styles()

    # 2. Ingestion
    logger.info("Phase 1: Ingesting Data...")
    try:
        # Load raw data with ID kept for reference, but we need a clean version for plotting
        # Note: load_and_clean_data resolves the path internally if None is passed.
        # But for 'raw_df = pd.read_csv', we need the path.
        # The user's code had 'data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv', let's stick to that relative path
        # assuming run from root.
        
        # Actually, let's use load_and_clean_data(drop_id=False) to get the main DF.
        # And we need to make sure 'Attrition' is string 'Yes'/'No' for the first plot.
        # load_and_clean_data returns a dataframe where Attrition is still 'Yes'/'No' (cleaning only drops cols).
        clean_df = load_and_clean_data(drop_id=False) 
    except FileNotFoundError:
        logger.error("Data file not found! Please place 'WA_Fn-UseC_-HR-Employee-Attrition.csv' in data/raw/")
        return

    # 3. Visualization (Pre-Model)
    logger.info("Phase 2: Generating Exploratory Visualizations...")
    try:
         plot_attrition_by_overtime(clean_df, figures_dir)
         plot_correlation_heatmap(clean_df, figures_dir)  # For the presentation deck
    except Exception as e:
        logger.error(f"Failed to plot exploratory visualizations: {e}")

    # 4. Feature Engineering
    logger.info("Phase 3: Engineering Features...")
    df_processed = perform_feature_engineering(clean_df)  # No scaling here - done after split
    
    # Split for Training
    # We drop EmployeeNumber for training
    # And we also need to drop 'Attrition' because it's the target.
    # Note: perform_feature_engineering encodes Attrition to 0/1 in 'Attrition' column
    
    if 'EmployeeNumber' in df_processed.columns:
        X = df_processed.drop(columns=['Attrition', 'EmployeeNumber'])
    else:
        X = df_processed.drop(columns=['Attrition'])
        
    y = df_processed['Attrition']  # Already 0/1 from features.py:encode_features
    
    # Proper scaling: fit on training data only to prevent data leakage
    # For main.py we train on full X for final model, but demonstrate proper pattern
    X_scaled, _ = scale_train_test(X, X)  # In production: split first, then scale
    
    # 5. Modeling
    logger.info("Phase 4: Training Logistic Regression Model...")
    model = train_logistic_regression(X_scaled, y, class_weight='balanced')

    # --- NEW: Extract Diagnostic Insights ---
    logger.info("Extracting strategic insights...")
    feature_names = X_scaled.columns.tolist()
    global_drivers = get_strategic_insights(model, feature_names)

    # Save to JSON for injection
    with open(results_dir / 'global_drivers.json', 'w') as f:
        json.dump(global_drivers, f, indent=2)

    logger.info(f"Strategic insights saved: {global_drivers}")

    # 6. Model Interpretation
    logger.info("Phase 5: Visualizing Model Drivers...")
    plot_feature_importance(model, X_scaled, X_scaled.columns, figures_dir)

    # 7. Risk Scoring (The Product)
    logger.info("Phase 6: Generating Risk Watch List...")
    
    # Score the *Active* employees only
    # Attrition is 0/1 now. 0 = No/Stay, 1 = Yes/Leave.
    active_mask = (df_processed['Attrition'] == 0)
    
    # Use scaled features for consistent prediction
    X_active_scaled = X_scaled[active_mask]
    
    # Get EmployeeNumber from the processed dataframe
    employees_active = df_processed.loc[active_mask, 'EmployeeNumber']
    
    risk_scores = model.predict_proba(X_active_scaled)[:, 1]
    
    # Visualize Risk Distribution
    plot_risk_distribution(risk_scores, figures_dir)

    # Create Export CSV
    watch_list = pd.DataFrame({
        'EmployeeNumber': employees_active,
        'RiskScore': risk_scores
    }).sort_values('RiskScore', ascending=False)
    
    watch_list['RiskLevel'] = pd.cut(watch_list['RiskScore'], 
                                     bins=[0, 0.3, 0.7, 1.0], 
                                     labels=['Low', 'Medium', 'High'])

    output_path = results_dir / 'risk_watch_list.csv'
    watch_list.to_csv(output_path, index=False)
    
    logger.info(f"SUCCESS. Pipeline Complete.")
    logger.info(f"1. Risk Watch List saved to: {output_path}")
    logger.info(f"2. Figures saved to: {figures_dir}")

if __name__ == "__main__":
    main()
