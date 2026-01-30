import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, OrdinalEncoder
from typing import Tuple, List

def calculate_tenure_ratio(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates 'TenureRatio': YearsAtCompany / TotalWorkingYears
    Handles division by zero by replacing with 0.
    Uses vectorized numpy operations for performance.
    """
    df = df.copy()
    # Vectorized: 10-100x faster than row-wise apply()
    df['TenureRatio'] = np.where(
        df['TotalWorkingYears'] > 0,
        df['YearsAtCompany'] / df['TotalWorkingYears'],
        0
    )
    return df

def calculate_promotion_stagnation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates 'PromotionStagnation': YearsInCurrentRole - YearsSinceLastPromotion
    """
    df = df.copy()
    df['PromotionStagnation'] = df['YearsInCurrentRole'] - df['YearsSinceLastPromotion']
    return df

def calculate_income_stability(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates 'IncomeStability': MonthlyIncome / Age
    """
    df = df.copy()
    df['IncomeStability'] = df['MonthlyIncome'] / df['Age']
    return df

def calculate_satisfaction_composite(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates 'SatisfactionComposite': Mean of Job, Environment, Relationship Satisfaction, and WorkLifeBalance.
    """
    df = df.copy()
    cols = ['JobSatisfaction', 'EnvironmentSatisfaction', 'RelationshipSatisfaction', 'WorkLifeBalance']
    df['SatisfactionComposite'] = df[cols].mean(axis=1)
    return df

def encode_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """
    Applies One-Hot Encoding to nominal variables and Label Encoding to target.
    Ordinal variables are left as is (since they are already 1-5).
    """
    df = df.copy()
    
    # 1. Label Encode Target
    if 'Attrition' in df.columns:
        df['Attrition'] = df['Attrition'].map({'Yes': 1, 'No': 0})
        
    # 2. One-Hot Encoding
    nominal_cols = ['Department', 'JobRole', 'MaritalStatus', 'EducationField', 'Gender', 'BusinessTravel']
    # 'OverTime' is binary Yes/No, map it manually or OHE. Let's map it.
    if 'OverTime' in df.columns:
        df['OverTime'] = df['OverTime'].map({'Yes': 1, 'No': 0})
        
    # Get dummies
    df = pd.get_dummies(df, columns=nominal_cols, drop_first=True)
    
    return df

def scale_features(df: pd.DataFrame, target_col: str = 'Attrition') -> pd.DataFrame:
    """
    Scales numerical features using MinMaxScaler.
    Excludes the target column and EmployeeNumber if present.
    """
    df = df.copy()
    scaler = MinMaxScaler()
    
    exclusions = [target_col, 'EmployeeNumber']
    feature_cols = [c for c in df.columns if c not in exclusions]
    
    df[feature_cols] = scaler.fit_transform(df[feature_cols])
    return df

def scale_train_test(X_train: pd.DataFrame, X_test: pd.DataFrame, 
                     target_col: str = 'Attrition') -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Properly scales features by fitting ONLY on training data.
    This prevents data leakage from test set into training.
    
    Args:
        X_train: Training features (already split)
        X_test: Test features (already split)
        target_col: Target column name to exclude from scaling
        
    Returns:
        Tuple of (X_train_scaled, X_test_scaled)
    """
    scaler = MinMaxScaler()
    
    # Exclude target and ID columns if present
    exclusions = [target_col, 'EmployeeNumber']
    feature_cols = [c for c in X_train.columns if c not in exclusions]
    
    # Fit on TRAIN only - this is the key to preventing leakage
    scaler.fit(X_train[feature_cols])
    
    # Transform both using the scaler fitted on train
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    
    X_train_scaled[feature_cols] = scaler.transform(X_train[feature_cols])
    X_test_scaled[feature_cols] = scaler.transform(X_test[feature_cols])
    
    return X_train_scaled, X_test_scaled

def perform_feature_engineering(df: pd.DataFrame, scale: bool = False) -> pd.DataFrame:
    """
    Pipeline wrapper for feature construction and encoding steps.
    
    Args:
        df: Input dataframe
        scale: If True, applies scaling (NOT recommended - use scale_train_test instead)
    
    Returns:
        Encoded dataframe ready for train/test split
    
    Note:
        Scaling should be done AFTER splitting to prevent data leakage.
        Use scale_train_test() function after splitting.
    """
    # 1. Feature Construction
    df = calculate_tenure_ratio(df)
    df = calculate_promotion_stagnation(df)
    df = calculate_income_stability(df)
    df = calculate_satisfaction_composite(df)
    
    # 2. Encoding
    df = encode_features(df)
    
    # 3. Scaling - Only if explicitly requested (legacy support)
    # WARNING: Scaling before split causes data leakage!
    if scale:
        df = scale_features(df)
    
    return df

def split_data(df: pd.DataFrame, target_col: str = 'Attrition') -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Performs Stratified Split (80/20).
    """
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    for train_index, test_index in split.split(X, y):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        
    return X_train, X_test, y_train, y_test
