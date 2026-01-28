"""
Pytest Configuration

Fixtures and configuration for the test suite.
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'numeric_1': np.random.randn(100),
        'numeric_2': np.random.randint(0, 100, 100),
        'category': np.random.choice(['A', 'B', 'C'], 100),
        'with_missing': np.where(np.random.random(100) > 0.8, np.nan, np.random.randn(100))
    })


@pytest.fixture
def classification_data():
    """Create sample classification data."""
    np.random.seed(42)
    X = np.random.randn(200, 5)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    return X, y


@pytest.fixture
def regression_data():
    """Create sample regression data."""
    np.random.seed(42)
    X = np.random.randn(200, 5)
    y = 3 * X[:, 0] + 2 * X[:, 1] + np.random.randn(200) * 0.5
    return X, y
