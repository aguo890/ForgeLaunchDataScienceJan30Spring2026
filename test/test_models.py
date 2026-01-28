"""
Tests for Model Modules
"""

import pytest
import numpy as np

from models.classifiers import train_classifier, evaluate_classifier
from models.regressors import train_regressor, evaluate_regressor


class TestClassifiers:
    """Tests for classification models."""
    
    def test_logistic_regression(self, classification_data):
        """Test logistic regression training."""
        X, y = classification_data
        
        result = train_classifier(X, y, model_type='logistic')
        
        assert 'model' in result
        assert 'metrics' in result
        assert result['metrics']['accuracy'] > 0.5
    
    def test_random_forest_classifier(self, classification_data):
        """Test random forest classifier training."""
        X, y = classification_data
        
        result = train_classifier(X, y, model_type='random_forest')
        
        assert result['metrics']['accuracy'] > 0.5
        assert result['metrics']['precision'] >= 0
        assert result['metrics']['recall'] >= 0
    
    def test_evaluate_classifier(self, classification_data):
        """Test classifier evaluation metrics."""
        y_true = np.array([0, 1, 1, 0, 1, 0])
        y_pred = np.array([0, 1, 0, 0, 1, 1])
        
        metrics = evaluate_classifier(y_true, y_pred)
        
        assert 'accuracy' in metrics
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1' in metrics
        assert 0 <= metrics['accuracy'] <= 1


class TestRegressors:
    """Tests for regression models."""
    
    def test_linear_regression(self, regression_data):
        """Test linear regression training."""
        X, y = regression_data
        
        result = train_regressor(X, y, model_type='linear')
        
        assert 'model' in result
        assert 'metrics' in result
        assert result['metrics']['r2'] > 0.5
    
    def test_random_forest_regressor(self, regression_data):
        """Test random forest regressor training."""
        X, y = regression_data
        
        result = train_regressor(X, y, model_type='random_forest')
        
        assert result['metrics']['r2'] > 0
        assert result['metrics']['mse'] >= 0
        assert result['metrics']['mae'] >= 0
    
    def test_evaluate_regressor(self):
        """Test regressor evaluation metrics."""
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.1, 2.1, 2.9, 4.2, 4.8])
        
        metrics = evaluate_regressor(y_true, y_pred)
        
        assert 'mse' in metrics
        assert 'rmse' in metrics
        assert 'mae' in metrics
        assert 'r2' in metrics
        assert metrics['mse'] >= 0
        assert metrics['rmse'] >= 0


class TestModelEdgeCases:
    """Tests for edge cases in model training."""
    
    def test_small_dataset(self):
        """Test with minimal dataset."""
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
        y = np.array([0, 1, 0, 1, 0])
        
        result = train_classifier(X, y, model_type='logistic', test_size=0.4)
        
        assert 'model' in result
        assert 'metrics' in result
    
    def test_invalid_model_type(self, classification_data):
        """Test with invalid model type."""
        X, y = classification_data
        
        with pytest.raises(ValueError):
            train_classifier(X, y, model_type='invalid_model')
