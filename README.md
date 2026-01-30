# Strategic Data Science Sprint: HR Retention Analytics
**Forge Launch Skills Challenge - January 2026**

---

## Executive Summary

This project transforms a static HR dataset into a proactive **"Pre-Mortem" Retention System**. 
Using Logistic Regression, we identify employees at risk of leaving *before* they resign.

| Deliverable | Location | Description |
|-------------|----------|-------------|
| **Risk Watch List** | `results/risk_watch_list.csv` | Prioritized list of at-risk employees |
| **Visualizations** | `results/figures/` | 4 presentation-ready charts |
| **Reproducible Pipeline** | `main.py` | Single command reproduces all results |

---

## Technical Highlights

### 🚀 Performance Optimizations
- **Vectorized Operations**: Feature engineering uses `np.where()` for C-level performance, avoiding slow row-wise iteration

### 🔒 Data Integrity
- **No Data Leakage**: `scale_train_test()` fits the scaler on training data only, ensuring authentic model performance metrics

### 📊 Interpretable Model Choice
- **Logistic Regression**: Selected over black-box models because HR stakeholders need to understand *why* an employee is at risk. Coefficients act as "impact weights" for each driver.

---

## Directory Structure

```
├── data/
│   └── raw/                    # WA_Fn-UseC_-HR-Employee-Attrition.csv
├── notebooks/
│   ├── 01_EDA.ipynb            # Exploratory analysis
│   ├── 02_Feature_Engineering.ipynb
│   ├── 03_Modeling.ipynb
│   └── 04_Risk_Watch_List.ipynb
├── results/
│   ├── figures/
│   │   ├── 00_correlation_heatmap.png
│   │   ├── 01_overtime_impact.png
│   │   ├── 02_feature_drivers.png
│   │   └── 03_risk_distribution.png
│   └── risk_watch_list.csv
├── src/
│   ├── data_ingestion.py       # Loading & cleaning
│   ├── features.py             # Feature engineering + scaling
│   ├── modeling.py             # Model training & evaluation
│   └── visualization.py        # Plotting utilities
├── test/                       # Unit tests
├── main.py                     # MASTER ORCHESTRATOR
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Pipeline
```bash
python main.py
```

### 3. View Results
- **Charts:** `results/figures/`
- **Risk Watch List:** `results/risk_watch_list.csv`

---

## Feature Engineering

| Feature | Formula | Business Logic |
|---------|---------|----------------|
| `TenureRatio` | YearsAtCompany / TotalWorkingYears | Measures company loyalty vs. career length |
| `PromotionStagnation` | YearsInRole - YearsSincePromotion | Detects career stagnation |
| `IncomeStability` | MonthlyIncome / Age | Normalizes compensation by career stage |
| `SatisfactionComposite` | Mean of 4 satisfaction scores | Aggregates sentiment signals |

---

## Key Insights

1. **Burnout Signal**: Employees working overtime leave at **~31%** vs **10%** for non-overtime
2. **Sales Risk**: Sales Representatives have the highest attrition rate by role
3. **Top Drivers**: OverTime, JobInvolvement, and EnvironmentSatisfaction emerge as key predictors

---

## Author

Built with a "story-first" data philosophy: *analyses exist to make decisions easier for the people who need them.*
