import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, OrdinalEncoder
from typing import Tuple, List

def calculate_tenure_ratio(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates 'TenureRatio': YearsAtCompany / TotalWorkingYears
    Handles division by zero by replacing with 0.
    """
    df = df.copy()
    # Avoid division by zero
    df['TenureRatio'] = df.apply(
        lambda row: row['YearsAtCompany'] / row['TotalWorkingYears'] if row['TotalWorkingYears'] > 0 else 0,
        axis=1
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

def perform_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pipeline wrapper for all feature engineering steps.
    """
    # 1. Feature Construction
    df = calculate_tenure_ratio(df)
    df = calculate_promotion_stagnation(df)
    df = calculate_income_stability(df)
    df = calculate_satisfaction_composite(df)
    
    # 2. Encoding
    df = encode_features(df)
    
    # 3. Scaling (Optional - mainly for Distance based models, but good for standardization)
    # Note: We tend to scale AFTER split to avoid leakage, but for this sprint we might do it here 
    # if we are careful, or better yet, return the unscaled processed data and scale in the pipeline.
    # The prompt says "Encoding and Scaling (Hour 19-22)".
    # Let's apply scaling here for simplicity as per the "Sprint" nature, 
    # BUT strictly speaking we should fit scaler on Train and transform Test.
    # Given the instructions, we'll return the encoded dataframe and let the modeling notebook handle splitting/scaling correctly 
    # OR follow the prompt's implicit flow. 
    # The prompt said: "Splitting: Enforcing a Stratified Split ... AFTER Encoding and Scaling".
    # So we will scale here.
    
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
