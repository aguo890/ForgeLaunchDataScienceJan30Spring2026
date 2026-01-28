"""
Exploratory Data Analysis (EDA) Utilities

This module provides functions for exploring and understanding datasets.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List, Dict, Any


def explore_dataframe(df: pd.DataFrame, verbose: bool = True) -> Dict[str, Any]:
    """
    Perform comprehensive exploration of a DataFrame.
    
    Args:
        df: Input DataFrame to explore
        verbose: If True, print summary to console
        
    Returns:
        Dictionary containing exploration results
    """
    results = {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.to_dict(),
        'missing': df.isnull().sum().to_dict(),
        'missing_pct': (df.isnull().sum() / len(df) * 100).to_dict(),
        'duplicates': df.duplicated().sum(),
        'memory_usage': df.memory_usage(deep=True).sum() / 1024**2  # MB
    }
    
    if verbose:
        print(f"📊 DataFrame Shape: {results['shape']}")
        print(f"📦 Memory Usage: {results['memory_usage']:.2f} MB")
        print(f"🔢 Columns: {len(results['columns'])}")
        print(f"❓ Total Missing: {sum(results['missing'].values())}")
        print(f"🔄 Duplicates: {results['duplicates']}")
    
    return results


def get_summary_statistics(
    df: pd.DataFrame, 
    columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Generate comprehensive summary statistics for numeric columns.
    
    Args:
        df: Input DataFrame
        columns: Specific columns to analyze (defaults to all numeric)
        
    Returns:
        DataFrame with summary statistics
    """
    if columns is None:
        numeric_df = df.select_dtypes(include=[np.number])
    else:
        numeric_df = df[columns].select_dtypes(include=[np.number])
    
    stats = numeric_df.describe().T
    stats['median'] = numeric_df.median()
    stats['skew'] = numeric_df.skew()
    stats['kurtosis'] = numeric_df.kurtosis()
    stats['iqr'] = stats['75%'] - stats['25%']
    
    return stats


def plot_distributions(
    df: pd.DataFrame, 
    columns: Optional[List[str]] = None,
    figsize: tuple = (15, 10),
    bins: int = 30
) -> plt.Figure:
    """
    Plot distribution histograms for numeric columns.
    
    Args:
        df: Input DataFrame
        columns: Specific columns to plot (defaults to all numeric)
        figsize: Figure size tuple
        bins: Number of histogram bins
        
    Returns:
        Matplotlib figure object
    """
    if columns is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    else:
        numeric_cols = columns
    
    n_cols = min(3, len(numeric_cols))
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten() if n_rows * n_cols > 1 else [axes]
    
    for idx, col in enumerate(numeric_cols):
        ax = axes[idx]
        df[col].dropna().hist(bins=bins, ax=ax, edgecolor='black', alpha=0.7)
        ax.set_title(f'{col}')
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
    
    # Hide empty subplots
    for idx in range(len(numeric_cols), len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    return fig


def correlation_analysis(
    df: pd.DataFrame,
    method: str = 'pearson',
    threshold: float = 0.5,
    figsize: tuple = (12, 10)
) -> Dict[str, Any]:
    """
    Perform correlation analysis and identify highly correlated features.
    
    Args:
        df: Input DataFrame
        method: Correlation method ('pearson', 'spearman', 'kendall')
        threshold: Threshold for flagging high correlations
        figsize: Figure size for heatmap
        
    Returns:
        Dictionary with correlation matrix and high correlation pairs
    """
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr(method=method)
    
    # Find high correlations
    high_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            if abs(corr_matrix.iloc[i, j]) > threshold:
                high_corr.append({
                    'feature_1': corr_matrix.columns[i],
                    'feature_2': corr_matrix.columns[j],
                    'correlation': corr_matrix.iloc[i, j]
                })
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        corr_matrix, 
        annot=True, 
        fmt='.2f', 
        cmap='RdBu_r',
        center=0,
        ax=ax
    )
    ax.set_title(f'{method.capitalize()} Correlation Matrix')
    plt.tight_layout()
    
    return {
        'matrix': corr_matrix,
        'high_correlations': pd.DataFrame(high_corr),
        'figure': fig
    }
