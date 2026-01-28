"""
Tests for EDA and Preprocessing Modules
"""

import pytest
import pandas as pd
import numpy as np

from analysis.eda import (
    explore_dataframe,
    get_summary_statistics,
    correlation_analysis
)
from analysis.preprocessing import (
    handle_missing_values,
    detect_outliers,
    validate_data_types
)


class TestExploreDataframe:
    """Tests for explore_dataframe function."""
    
    def test_basic_exploration(self, sample_dataframe):
        """Test basic DataFrame exploration."""
        results = explore_dataframe(sample_dataframe, verbose=False)
        
        assert 'shape' in results
        assert results['shape'] == (100, 4)
        assert 'columns' in results
        assert len(results['columns']) == 4
    
    def test_missing_detection(self, sample_dataframe):
        """Test missing value detection."""
        results = explore_dataframe(sample_dataframe, verbose=False)
        
        assert 'missing' in results
        assert 'with_missing' in results['missing']
        assert results['missing']['with_missing'] > 0


class TestSummaryStatistics:
    """Tests for get_summary_statistics function."""
    
    def test_numeric_stats(self, sample_dataframe):
        """Test numeric summary statistics."""
        stats = get_summary_statistics(sample_dataframe)
        
        assert 'mean' in stats.columns
        assert 'std' in stats.columns
        assert 'median' in stats.columns
        assert 'skew' in stats.columns
    
    def test_specific_columns(self, sample_dataframe):
        """Test stats for specific columns."""
        stats = get_summary_statistics(sample_dataframe, columns=['numeric_1'])
        
        assert len(stats) == 1
        assert 'numeric_1' in stats.index


class TestHandleMissingValues:
    """Tests for handle_missing_values function."""
    
    def test_drop_strategy(self, sample_dataframe):
        """Test dropping missing values."""
        df_cleaned, changes = handle_missing_values(sample_dataframe, strategy='drop')
        
        assert df_cleaned['with_missing'].isnull().sum() == 0
        assert len(df_cleaned) < len(sample_dataframe)
    
    def test_mean_strategy(self, sample_dataframe):
        """Test mean imputation."""
        df_cleaned, changes = handle_missing_values(sample_dataframe, strategy='mean')
        
        # Only numeric columns with missing are filled
        assert df_cleaned['with_missing'].isnull().sum() == 0


class TestDetectOutliers:
    """Tests for detect_outliers function."""
    
    def test_iqr_method(self, sample_dataframe):
        """Test IQR outlier detection."""
        outliers = detect_outliers(sample_dataframe, method='iqr')
        
        assert 'numeric_1' in outliers
        assert 'count' in outliers['numeric_1']
        assert 'lower_bound' in outliers['numeric_1']
        assert 'upper_bound' in outliers['numeric_1']
    
    def test_zscore_method(self, sample_dataframe):
        """Test Z-score outlier detection."""
        outliers = detect_outliers(sample_dataframe, method='zscore', threshold=3)
        
        assert 'numeric_1' in outliers


class TestValidateDataTypes:
    """Tests for validate_data_types function."""
    
    def test_valid_types(self, sample_dataframe):
        """Test type validation with correct types."""
        expected = {
            'numeric_1': float,
            'numeric_2': int
        }
        
        results = validate_data_types(sample_dataframe, expected)
        
        assert 'numeric_1' in results
        assert 'numeric_2' in results
    
    def test_missing_column(self, sample_dataframe):
        """Test validation with missing column."""
        expected = {'nonexistent_column': str}
        
        results = validate_data_types(sample_dataframe, expected)
        
        assert results['nonexistent_column']['valid'] is False
        assert 'not found' in results['nonexistent_column']['error']
