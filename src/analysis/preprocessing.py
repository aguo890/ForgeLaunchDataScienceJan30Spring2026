"""
Data Preprocessing Utilities

This module provides functions for data cleaning and preprocessing.
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Literal, Tuple


def handle_missing_values(
    df: pd.DataFrame,
    strategy: Literal['drop', 'mean', 'median', 'mode', 'constant'] = 'drop',
    columns: Optional[List[str]] = None,
    fill_value: Optional[any] = None,
    threshold: float = 0.5
) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """
    Handle missing values in a DataFrame.
    
    Args:
        df: Input DataFrame
        strategy: How to handle missing values
            - 'drop': Drop rows with missing values
            - 'mean': Fill with column mean (numeric only)
            - 'median': Fill with column median (numeric only)
            - 'mode': Fill with column mode
            - 'constant': Fill with specified constant
        columns: Specific columns to process (defaults to all)
        fill_value: Value to use when strategy is 'constant'
        threshold: Drop columns with missing % above threshold (0-1)
        
    Returns:
        Tuple of (processed DataFrame, dict of changes made)
    """
    df = df.copy()
    changes = {}
    
    if columns is None:
        columns = df.columns.tolist()
    
    # First, drop columns with too many missing values
    missing_pct = df[columns].isnull().sum() / len(df)
    cols_to_drop = missing_pct[missing_pct > threshold].index.tolist()
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
        changes['columns_dropped'] = len(cols_to_drop)
        columns = [c for c in columns if c not in cols_to_drop]
    
    initial_missing = df[columns].isnull().sum().sum()
    
    if strategy == 'drop':
        df = df.dropna(subset=columns)
    elif strategy == 'mean':
        numeric_cols = df[columns].select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif strategy == 'median':
        numeric_cols = df[columns].select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    elif strategy == 'mode':
        for col in columns:
            if df[col].isnull().any():
                mode_val = df[col].mode()
                if len(mode_val) > 0:
                    df[col] = df[col].fillna(mode_val[0])
    elif strategy == 'constant':
        df[columns] = df[columns].fillna(fill_value)
    
    final_missing = df[columns].isnull().sum().sum() if columns else 0
    changes['values_handled'] = initial_missing - final_missing
    changes['remaining_missing'] = final_missing
    
    return df, changes


def detect_outliers(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    method: Literal['iqr', 'zscore'] = 'iqr',
    threshold: float = 1.5
) -> Dict[str, Dict]:
    """
    Detect outliers in numeric columns.
    
    Args:
        df: Input DataFrame
        columns: Specific columns to analyze (defaults to all numeric)
        method: Detection method
            - 'iqr': Interquartile Range method
            - 'zscore': Standard deviation method
        threshold: Threshold for outlier detection
            - For IQR: multiplier (default 1.5)
            - For zscore: number of standard deviations (default 3)
            
    Returns:
        Dictionary with outlier information per column
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    outlier_info = {}
    
    for col in columns:
        series = df[col].dropna()
        
        if method == 'iqr':
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr
            outliers = series[(series < lower_bound) | (series > upper_bound)]
        else:  # zscore
            mean = series.mean()
            std = series.std()
            z_scores = np.abs((series - mean) / std)
            outliers = series[z_scores > threshold]
            lower_bound = mean - threshold * std
            upper_bound = mean + threshold * std
        
        outlier_info[col] = {
            'count': len(outliers),
            'percentage': len(outliers) / len(series) * 100,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'indices': outliers.index.tolist()
        }
    
    return outlier_info


def validate_data_types(
    df: pd.DataFrame,
    expected_types: Dict[str, type]
) -> Dict[str, Dict]:
    """
    Validate that columns have expected data types.
    
    Args:
        df: Input DataFrame
        expected_types: Dictionary mapping column names to expected types
        
    Returns:
        Validation results dictionary
    """
    results = {}
    
    for col, expected_type in expected_types.items():
        if col not in df.columns:
            results[col] = {
                'valid': False,
                'error': 'Column not found',
                'actual_type': None
            }
            continue
        
        actual_type = df[col].dtype
        
        # Map pandas dtypes to Python types for comparison
        type_mapping = {
            'int64': int,
            'float64': float,
            'object': str,
            'bool': bool,
            'datetime64[ns]': 'datetime'
        }
        
        is_valid = str(actual_type) in [
            k for k, v in type_mapping.items() 
            if v == expected_type or str(v) == str(expected_type)
        ]
        
        results[col] = {
            'valid': is_valid,
            'expected': str(expected_type),
            'actual_type': str(actual_type),
            'sample_values': df[col].head(3).tolist()
        }
    
    return results
