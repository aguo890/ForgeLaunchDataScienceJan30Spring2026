"""
Regression Models

This module provides regression model implementations and utilities.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Literal
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    mean_absolute_percentage_error
)
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR


def train_regressor(
    X: np.ndarray,
    y: np.ndarray,
    model_type: Literal['linear', 'ridge', 'lasso', 'elastic_net', 'random_forest', 'gradient_boost', 'svr'] = 'random_forest',
    test_size: float = 0.2,
    random_state: int = 42,
    **model_params
) -> Dict[str, Any]:
    """
    Train a regression model.
    
    Args:
        X: Feature matrix
        y: Target values
        model_type: Type of regressor to train
        test_size: Fraction of data for testing
        random_state: Random seed for reproducibility
        **model_params: Additional parameters for the model
        
    Returns:
        Dictionary containing model, predictions, and metrics
    """
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Select model
    models = {
        'linear': LinearRegression(**model_params),
        'ridge': Ridge(**model_params),
        'lasso': Lasso(**model_params),
        'elastic_net': ElasticNet(**model_params),
        'random_forest': RandomForestRegressor(n_estimators=100, **model_params),
        'gradient_boost': GradientBoostingRegressor(**model_params),
        'svr': SVR(**model_params)
    }
    
    model = models.get(model_type)
    if model is None:
        raise ValueError(f"Unknown model type: {model_type}")
    
    # Train
    model.fit(X_train, y_train)
    
    # Predict
    y_pred = model.predict(X_test)
    
    # Evaluate
    metrics = evaluate_regressor(y_test, y_pred)
    
    return {
        'model': model,
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'y_pred': y_pred,
        'metrics': metrics
    }


def evaluate_regressor(
    y_true: np.ndarray,
    y_pred: np.ndarray
) -> Dict[str, float]:
    """
    Evaluate regression model performance.
    
    Args:
        y_true: True values
        y_pred: Predicted values
        
    Returns:
        Dictionary of evaluation metrics
    """
    return {
        'mse': mean_squared_error(y_true, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
        'mae': mean_absolute_error(y_true, y_pred),
        'r2': r2_score(y_true, y_pred),
        'mape': mean_absolute_percentage_error(y_true, y_pred) * 100  # As percentage
    }


def cross_validate_regressor(
    model: Any,
    X: np.ndarray,
    y: np.ndarray,
    cv: int = 5,
    scoring: str = 'neg_mean_squared_error'
) -> Dict[str, float]:
    """
    Perform cross-validation for a regression model.
    
    Args:
        model: Scikit-learn compatible model
        X: Feature matrix
        y: Target values
        cv: Number of cross-validation folds
        scoring: Scoring metric
        
    Returns:
        Dictionary with CV results
    """
    scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
    
    return {
        'cv_scores': scores.tolist(),
        'mean_score': np.mean(scores),
        'std_score': np.std(scores)
    }
