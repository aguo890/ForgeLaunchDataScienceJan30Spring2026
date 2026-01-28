
import pandas as pd
import numpy as np
import shap
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, recall_score, f1_score
from imblearn.over_sampling import SMOTE
from typing import Tuple, Dict, Any

def load_processed_data(data_dir: str = 'data/processed') -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    Loads processed train/test parquet files.
    """
    train_path = f"{data_dir}/train.parquet"
    test_path = f"{data_dir}/test.parquet"
    
    train_df = pd.read_parquet(train_path)
    test_df = pd.read_parquet(test_path)
    
    # Assuming 'Attrition' is the target and it is the last column or named 'Attrition'
    target = 'Attrition'
    
    X_train = train_df.drop(columns=[target])
    y_train = train_df[target]
    
    X_test = test_df.drop(columns=[target])
    y_test = test_df[target]
    
    return X_train, y_train, X_test, y_test

def apply_smote(X_train: pd.DataFrame, y_train: pd.Series) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Applies SMOTE to training data to handle class imbalance.
    """
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
    return X_resampled, y_resampled

def train_logistic_regression(X_train, y_train, class_weight='balanced') -> LogisticRegression:
    """
    Trains a Logistic Regression model.
    """
    model = LogisticRegression(max_iter=1000, class_weight=class_weight, random_state=42)
    model.fit(X_train, y_train)
    return model

def train_xgboost(X_train, y_train, scale_pos_weight=None) -> XGBClassifier:
    """
    Trains an XGBoost model.
    """
    # If SMOTE is used, scale_pos_weight might not be needed, but good to have option.
    model = XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=4,
        use_label_encoder=False,
        eval_metric='logloss',
        random_state=42
    )
    if scale_pos_weight:
         model.set_params(scale_pos_weight=scale_pos_weight)
         
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test, model_name="Model") -> Dict[str, Any]:
    """
    Evaluates model performance and returns metrics.
    """
    y_pred = model.predict(X_test)
    
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"--- {model_name} Evaluation ---")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    return {'recall': recall, 'f1': f1}

def get_shap_values(model, X_data):
    """
    Calculates SHAP values for interpretation.
    """
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_data)
    return explainer, shap_values
