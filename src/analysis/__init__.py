"""
Forge Launch Data Science - Analysis Module

This module provides core data analysis utilities.
"""

from .eda import (
    explore_dataframe,
    get_summary_statistics,
    plot_distributions,
    correlation_analysis,
)

from .preprocessing import (
    handle_missing_values,
    detect_outliers,
    validate_data_types,
)

__all__ = [
    'explore_dataframe',
    'get_summary_statistics', 
    'plot_distributions',
    'correlation_analysis',
    'handle_missing_values',
    'detect_outliers',
    'validate_data_types',
]
