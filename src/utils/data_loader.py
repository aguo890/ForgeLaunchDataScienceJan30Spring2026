"""
Data Loading Utilities

This module provides functions for loading data from various file formats.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any


def load_csv(
    path: str,
    **kwargs
) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame.
    
    Args:
        path: Path to the CSV file
        **kwargs: Additional arguments passed to pd.read_csv
        
    Returns:
        Loaded DataFrame
    """
    filepath = Path(path)
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    print(f"📥 Loading: {filepath.name}")
    df = pd.read_csv(filepath, **kwargs)
    print(f"✅ Loaded {len(df):,} rows, {len(df.columns)} columns")
    
    return df


def load_excel(
    path: str,
    sheet_name: Optional[str] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Load an Excel file into a DataFrame.
    
    Args:
        path: Path to the Excel file
        sheet_name: Specific sheet to load (defaults to first sheet)
        **kwargs: Additional arguments passed to pd.read_excel
        
    Returns:
        Loaded DataFrame
    """
    filepath = Path(path)
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    print(f"📥 Loading: {filepath.name}")
    df = pd.read_excel(filepath, sheet_name=sheet_name, **kwargs)
    print(f"✅ Loaded {len(df):,} rows, {len(df.columns)} columns")
    
    return df


def load_parquet(
    path: str,
    **kwargs
) -> pd.DataFrame:
    """
    Load a Parquet file into a DataFrame.
    
    Args:
        path: Path to the Parquet file
        **kwargs: Additional arguments passed to pd.read_parquet
        
    Returns:
        Loaded DataFrame
    """
    filepath = Path(path)
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    print(f"📥 Loading: {filepath.name}")
    df = pd.read_parquet(filepath, **kwargs)
    print(f"✅ Loaded {len(df):,} rows, {len(df.columns)} columns")
    
    return df


def save_processed_data(
    df: pd.DataFrame,
    path: str,
    format: str = 'parquet'
) -> None:
    """
    Save processed data to disk.
    
    Args:
        df: DataFrame to save
        path: Output file path
        format: File format ('parquet', 'csv')
    """
    filepath = Path(path)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    if format == 'parquet':
        df.to_parquet(filepath, index=False)
    elif format == 'csv':
        df.to_csv(filepath, index=False)
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    print(f"💾 Saved {len(df):,} rows to {filepath.name}")
