import pandas as pd
import logging
from pathlib import Path
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data(filepath: str) -> pd.DataFrame:
    """
    Loads data from a CSV file.
    
    Args:
        filepath (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: Loaded dataframe.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"The file {filepath} was not found.")
    
    logger.info(f"Loading data from {filepath}...")
    df = pd.read_csv(path)
    logger.info(f"Data loaded successfully. Shape: {df.shape}")
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs basic data hygiene:
    - Drops zero-variance columns (EmployeeCount, Over18, StandardHours)
    - Drops unique identifiers (EmployeeNumber)
    - Checks for duplicates
    
    Args:
        df (pd.DataFrame): Raw dataframe.
        
    Returns:
        pd.DataFrame: Cleaned dataframe.
    """
    logger.info("Starting data cleaning...")
    
    # List of columns to drop as identified in the Sprint Plan
    cols_to_drop = ['EmployeeCount', 'Over18', 'StandardHours', 'EmployeeNumber']
    
    # Drop existing columns from the list
    existing_cols_drop = [c for c in cols_to_drop if c in df.columns]
    
    if existing_cols_drop:
        df_cleaned = df.drop(columns=existing_cols_drop)
        logger.info(f"Dropped columns: {existing_cols_drop}")
    else:
        df_cleaned = df
        logger.info("No columns to drop found from the target list.")
        
    # Check duplicate rows
    duplicates = df_cleaned.duplicated().sum()
    if duplicates > 0:
        logger.warning(f"Found {duplicates} duplicate rows. Consider dropping them.")
    
    logger.info(f"Cleaning complete. New Shape: {df_cleaned.shape}")
    return df_cleaned

def load_and_clean_data(filepath: str = None) -> pd.DataFrame:
    """
    Convenience function to load and clean data in one step.
    Args:
        filepath (str): Path to raw data. If None, resolves relative to project root.
    Returns:
        pd.DataFrame: Cleaned dataframe.
    """
    if filepath is None:
        # Resolves to <project_root>/data/raw/...
        filepath = Path(__file__).resolve().parent.parent / "data" / "raw" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
    
    df = load_data(str(filepath))
    return clean_data(df)

if __name__ == "__main__":
    # Default execution for testing
    raw_data_path = Path("data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv")
    
    try:
        df = load_data(str(raw_data_path))
        df_clean = clean_data(df)
        
        # Save a sample or just verify
        print(df_clean.head())
        print(f"\nRemaining columns: {df_clean.columns.tolist()}")
        
    except Exception as e:
        logger.error(f"Error in data ingestion: {e}")
