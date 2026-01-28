"""
Classification Models

This module provides classification model implementations and utilities.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List, Literal
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC


def train_classifier(
    X: np.ndarray,
    y: np.ndarray,
    model_type: Literal['logistic', 'random_forest', 'gradient_boost', 'svm'] = 'random_forest',
    test_size: float = 0.2,
    random_state: int = 42,
    **model_params
) -> Dict[str, Any]:
    """
    Train a classification model.
    
    Args:
        X: Feature matrix
        y: Target labels
        model_type: Type of classifier to train
        test_size: Fraction of data for testing
        random_state: Random seed for reproducibility
        **model_params: Additional parameters for the model
        
    Returns:
        Dictionary containing model, predictions, and metrics
    """
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Select model
    models = {
        'logistic': LogisticRegression(max_iter=1000, **model_params),
        'random_forest': RandomForestClassifier(n_estimators=100, **model_params),
        'gradient_boost': GradientBoostingClassifier(**model_params),
        'svm': SVC(**model_params)
    }
    
    model = models.get(model_type)
    if model is None:
        raise ValueError(f"Unknown model type: {model_type}")
    
    # Train
    model.fit(X_train, y_train)
    
    # Predict
    y_pred = model.predict(X_test)
    
    # Evaluate
    metrics = evaluate_classifier(y_test, y_pred)
    
    return {
        'model': model,
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'y_pred': y_pred,
        'metrics': metrics
    }


def evaluate_classifier(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    average: str = 'weighted'
) -> Dict[str, float]:
    """
    Evaluate classification model performance.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        average: Averaging strategy for multiclass metrics
        
    Returns:
        Dictionary of evaluation metrics
    """
    return {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average=average, zero_division=0),
        'recall': recall_score(y_true, y_pred, average=average, zero_division=0),
        'f1': f1_score(y_true, y_pred, average=average, zero_division=0)
    }


def get_classification_report(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    target_names: Optional[List[str]] = None
) -> str:
    """
    Generate a detailed classification report.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        target_names: Optional names for classes
        
    Returns:
        Formatted classification report string
    """
    return classification_report(y_true, y_pred, target_names=target_names)


def get_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray
) -> np.ndarray:
    """
    Generate confusion matrix.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        
    Returns:
        Confusion matrix as numpy array
    """
    return confusion_matrix(y_true, y_pred)
