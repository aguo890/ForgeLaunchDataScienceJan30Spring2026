"""
Base Model Class

This module provides a base class for all machine learning models.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import numpy as np
import pandas as pd
import pickle
from pathlib import Path


class BaseModel(ABC):
    """
    Abstract base class for machine learning models.
    
    Provides a consistent interface for training, prediction, and evaluation.
    """
    
    def __init__(self, name: str, **kwargs):
        """
        Initialize the base model.
        
        Args:
            name: Model identifier name
            **kwargs: Additional model configuration
        """
        self.name = name
        self.model = None
        self.is_fitted = False
        self.config = kwargs
        self.metrics: Dict[str, float] = {}
    
    @abstractmethod
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'BaseModel':
        """
        Train the model on the provided data.
        
        Args:
            X: Training features
            y: Training targets
            
        Returns:
            Self for method chaining
        """
        pass
    
    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions on new data.
        
        Args:
            X: Features for prediction
            
        Returns:
            Predicted values
        """
        pass
    
    @abstractmethod
    def evaluate(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """
        Evaluate model performance on test data.
        
        Args:
            X: Test features
            y: True target values
            
        Returns:
            Dictionary of evaluation metrics
        """
        pass
    
    def save(self, path: str) -> None:
        """
        Save the model to disk.
        
        Args:
            path: File path for saving the model
        """
        if not self.is_fitted:
            raise ValueError("Cannot save unfitted model")
        
        filepath = Path(path)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump({
                'name': self.name,
                'model': self.model,
                'config': self.config,
                'metrics': self.metrics
            }, f)
        
        print(f"✅ Model saved to {filepath}")
    
    @classmethod
    def load(cls, path: str) -> 'BaseModel':
        """
        Load a model from disk.
        
        Args:
            path: File path to load from
            
        Returns:
            Loaded model instance
        """
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        instance = cls.__new__(cls)
        instance.name = data['name']
        instance.model = data['model']
        instance.config = data['config']
        instance.metrics = data['metrics']
        instance.is_fitted = True
        
        return instance
    
    def __repr__(self) -> str:
        status = "fitted" if self.is_fitted else "unfitted"
        return f"{self.__class__.__name__}(name='{self.name}', status={status})"
