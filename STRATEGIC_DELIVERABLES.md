# Strategic Data Science Sprint: Deliverables

## Part 1: Executive Slide Deck (Content)
**Target Audience**: CHRO & CFO
**Objective**: Moving from reactive "Post-Mortems" to proactive "Pre-Mortems".

### Slide 1: Title
**Project Retention: Quantifying and Mitigating Workforce Churn**
*Strategic Intelligence for HR Optimization*

### Slide 2: Executive Summary
- **Scope**: Analyzed 1,470 employee records to identify retention risks.
- **Current State**: 16% Attrition Rate (237 Leavers).
- **Key Insight**: Attrition is driven by manageable factors—Burnout (OverTime) and Stagnation (Role Tenure).
- **Value**: Interpretable AI model identifies leavers with actionable risk scores.

### Slide 3: The Data Landscape
- **Foundation**: 35 Features analyzed across Demographics, Financials, and Operations.
- **Rigor**: rigorous hygiene applied; zero-variance noise removed.
- **Focus**: High-quality "Canonical Benchmark" data used to ensure validity.

### Slide 4: Who is Leaving? (Cohorts)
- **High Risk**: Sales Representatives and Laboratory Technicians.
- **Distribution**: Younger employees are more volatile, but senior attrition is more costly.
- **Metric**: Sales Reps show attrition rates significantly above the remaining workforce.

### Slide 5: Why are they Leaving? (Drivers)
- **Burnout**: Employees working OverTime have a **30.5%** attrition rate (vs ~10% for others).
- **Compensation**: Lower monthly income correlates with higher churn, but "Golden Handcuffs" apply to senior tiers.
- **Stagnation**: Employees stuck in role without promotion are flight risks.

### Slide 6: The Predictive Model
- **Technology**: Benchmarked Logistic Regression vs XGBoost (with SMOTE).
- **Performance**: Logistic Regression achieved a **Recall of 62%**, effectively capturing nearly 2/3rds of all potential leavers.
- **Logic**: It is better to intervene with a satisfied employee (False Positive) than lose a critical one (False Negative).

### Slide 7: The "Watch List" Strategy
- **Result**: Generated a probability score for every employee.
- **Action**: HR Dashboard can flag "High Risk" individuals for proactive retention interviews.
- **Ethics**: Scores are indicators for support, not penalties.

### Slide 8: Strategic Recommendations
1. **Immediate**: Audit "OverTime" allocation in Sales. Cap hours or hire relief.
2. **Medium Term**: Review compensation bands for Job Level 1 (Junior) to combat early exit.
3. **Long Term**: Implement "Rotation Programs" to reset `YearsInCurrentRole` clock and reduce stagnation.

### Slide 9: Societal Connection
- **Gig Economy**: High `NumCompaniesWorked` indicates a transactional relationship with employment.
- **RTO Friction**: `DistanceFromHome` is a latent risk factor for Return-to-Office mandates.

### Slide 10: Next Steps
- **Deploy**: Integrate model inference into weekly HR reports.
- **Validate**: Conduct exit interviews to confirm "EnvironmentSatisfaction" signals.
- **Iterate**: Re-train model quarterly with new data.

---

## Part 2: Technical Essays

### Essay 1: Methodological Rigor and Model Selection
**Abstract**
This project utilized the IBM HR Analytics dataset to predict employee attrition. Given the class imbalance (16% Attrition), standard accuracy metrics were discarded in favor of Recall and F1-Score.

**Preprocessing & Feature Engineering**
We engineered behavior-focused features:
- `TenureRatio` (Loyalty proxy)
- `PromotionStagnation` (Frustration proxy)
- `IncomeStability` (Financial health)
Categorical variables were handled via One-Hot Encoding, and the target was Label Encoded.

**Modeling Strategy**
We gathered a baseline using Logistic Regression with balanced class weights. The final model recommendations considered both linear and tree-based approaches.
- **SMOTE**: Applied to the training fold to address the 16% imbalance, synthesizing minority class examples.
- **Performance**: In this sprint, the **Logistic Regression (Class Weighted)** model provided superior Recall (0.62) compared to the tree-based ensemble (0.34), likely due to the linear separability of the primary drivers (OverTime, Income) and the small dataset size.

**Validation**
The model was evaluated on a held-out stratified test set (20%). Key performance indicators focused on Recall to capture the maximum number of potential leavers.

### Essay 2: Ethical Implications
Predictive modeling in HR requires a "Human-in-the-Loop" approach. The model predicts *risk*, not *destiny*.
- **Bias**: We monitored for protected class bias (Gender, Age).
- **Usage**: Output should trigger supportive actions (Retention Bonuses, Stay Interviews), never punitive actions.
- **Transparency**: SHAP values provide "Right to Explanation" for every prediction.
