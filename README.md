# Strategic Data Science Sprint: HR Retention Analytics
**Forge Launch Skills Challenge - Jan 2026**

## 1. Project Overview
This project transforms a static HR dataset into a proactive "Pre-Mortem" Retention System. 
Using Logistic Regression, we identify employees at risk of leaving *before* they resign.

**Key Deliverable:** `results/risk_watch_list.csv` (A prioritized list of at-risk employees).

## 2. Directory Structure

```
├── data/
│   └── raw/               # Place WA_Fn-UseC_-HR-Employee-Attrition.csv here
├── notebooks/             # Exploratory Analysis (EDAs)
├── results/
│   ├── figures/           # Generated charts for the slide deck
│   └── risk_watch_list.csv # Final output
├── src/
│   ├── data_ingestion.py  # Loading & cleaning
│   ├── features.py        # Feature engineering (TenureRatio, etc.)
│   ├── modeling.py        # Model training
│   └── visualization.py   # Plotting utilities
├── main.py                # MASTER SCRIPT - Run this to reproduce everything
├── requirements.txt       # Dependencies
└── README.md
```

## 3. Quick Start (Reproducibility)
To run the entire pipeline (Data Cleaning -> Modeling -> Visualization):

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Orchestrator:**
   ```bash
   python main.py
   ```

3. **View Results:**
   Check the `results/figures` folder for charts and `results/risk_watch_list.csv` for the findings.
