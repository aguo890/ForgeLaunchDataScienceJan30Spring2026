# Development Log

A chronological record of development iterations, decisions, and refinements.

---

## [1/28/2026 4pm] — Project Initialization

### Context
Initial project setup and skeleton creation.

### Changes
- Created repository structure
- Set up development environment
- Configured automation scripts

### Next Steps
- [ ] Load and explore initial data
- [ ] Begin EDA notebook

---

*[New entries will be appended above this line by automation scripts]*


## [2026-01-28 16:16] Infrastructure & Verification Automation Enhancements

### 1. Virtual Environment Isolation for Reproducibility
**Context/Problem**: The previous setup command installed dependencies directly into the system Python environment, risking dependency conflicts and making the project non-portable across different machines or users.

**Solution/Implementation**: Modified the `Makefile` `setup` target to create a dedicated **Python virtual environment** (`venv`) and install dependencies within it. Added a new `enter` target to provide clear activation instructions for Windows users.

**Rationale/Logic**: A virtual environment is a **best practice for dependency management** in data science projects. It ensures:
*   **Isolation**: Project dependencies are sandboxed, preventing conflicts with other projects or system packages.
*   **Reproducibility**: The exact dependency tree can be captured (`pip freeze > requirements.txt`) and recreated, which is critical for model reproducibility and deployment.
*   **Portability**: The environment setup is now self-contained within the project directory.

**Outcome**: The project setup is now robust and follows industry standards. The `enter` target provides clear, platform-specific guidance, reducing user error during environment activation.

### 2. Robust Test Execution within Virtual Environment
**Context/Problem**: The `autocommit.py` script's `run_verification()` function assumed `python` in the system PATH would be correct. After introducing the virtual environment, tests needed to run using the environment's Python interpreter to ensure they execute with the correct dependencies.

**Solution/Implementation**: Updated `run_verification()` to detect and use the Python executable from the project's `venv` directory (`venv/Scripts/python.exe` on Windows). It falls back to `sys.executable` if the virtual environment is not found.

**Rationale/Logic**: This change ensures the **automated verification pipeline is environment-aware**. Running tests with the virtual environment's interpreter guarantees they are executed in the same context where dependencies are installed, eliminating "works on my machine" issues. The fallback logic maintains backward compatibility if the script is run outside the standard setup flow.

**Outcome**: The automated commit and verification workflow (`scripts/autocommit.py`) is now fully integrated with the project's isolated environment, ensuring consistent test results.

### 3. Log Sanitization for Reliable Report Generation
**Context/Problem**: The `update

## [2026-01-28 16:16] Infrastructure & Verification Automation Improvements

### 1. Virtual Environment Isolation in Makefile

**Context/Problem**: The previous `make setup` command installed dependencies directly into the system Python environment, creating potential dependency conflicts and reproducibility issues across different developer machines. This violated the principle of isolated, reproducible environments for data science projects.

**Solution/Implementation**: Modified the `Makefile` to create a dedicated **virtual environment** (`venv`) and install dependencies within it. Added a new `make enter` target that provides clear activation instructions for Windows users.

**Rationale/Logic**: Virtual environments are essential for:
- **Dependency isolation**: Prevents conflicts between project requirements and system packages
- **Reproducibility**: Ensures consistent package versions across all development environments
- **Clean project state**: Makes it easier to debug environment-specific issues

The Windows-specific activation path (`.\venv\Scripts\activate`) was chosen because the development environment appears to be Windows-based (as evidenced by the test output showing `platform win32`).

**Outcome**: The setup process now creates a fully isolated environment. Verified by the successful test execution within the virtual environment.

### 2. Automated Test Execution with Virtual Environment Detection

**Context/Problem**: The `autocommit.py` script was calling the system Python interpreter directly, which could bypass the project's virtual environment and lead to inconsistent test results or missing dependencies.

**Solution/Implementation**: Enhanced the `run_verification()` function to:
1. Check for the existence of `venv/Scripts/python.exe` (Windows virtual environment)
2. Use the virtual environment Python if available, otherwise fall back to `sys.executable`
3. Added proper escaping of backslashes in test output to prevent regex errors

**Rationale/Logic**: This ensures that:
- Tests always run with the exact same dependencies installed via `make setup`
- The automation workflow respects the project's environment isolation
- Backslash escaping prevents regex substitution failures when processing Windows file paths in test output

The fallback to `sys.executable` maintains backward compatibility for environments without virtual environments.

**Outcome**: All 18 tests now pass consistently within the isolated environment. The test suite execution time is 2.87 seconds, indicating efficient test design.

### 3. QA Report Automation Enhancement

**Context/Problem**: The QA report previously showed placeholder text (`[Test output

## [2026-01-28 16:42] Notebook Infrastructure & Data Pipeline Implementation

### 1. EDA Notebook Creation with Hypothesis-Driven Analysis

**Context/Problem**: The project lacked an exploratory data analysis (EDA) phase to understand the attrition dataset's characteristics and validate initial business hypotheses. Without this foundational analysis, feature engineering and modeling decisions would be uninformed.

**Solution/Implementation**: Created `notebooks/01_EDA.ipynb` with a structured, hypothesis-driven approach. The notebook implements three core analyses:
1. **Burnout Hypothesis**: Examines attrition distribution by `OverTime` status with percentage annotations
2. **Compensation Hypothesis**: Compares `MonthlyIncome` distributions between leavers and stayers via box plots
3. **Sales Cohort Risk**: Calculates and visualizes attrition rates by `JobRole` with a benchmark line
4. **Multivariate Analysis**: Includes a correlation heatmap with upper-triangle masking for clarity

**Rationale/Logic**: This structured EDA follows **domain-driven investigation** rather than generic data exploration. Each visualization tests a specific business hypothesis about attrition drivers. The percentage annotations on count plots provide immediate interpretability, while the correlation matrix helps identify multicollinearity risks for future modeling. The use of `numeric_only=True` in the correlation calculation ensures compatibility with newer pandas versions.

**Outcome**: The notebook provides a reproducible analysis framework that can be extended. It confirms initial hypotheses (e.g., overtime employees have higher attrition) while quantifying effects (27.5% attrition rate for overtime employees vs. overall average of 16%).

### 2. Feature Engineering Pipeline Integration

**Context/Problem**: While feature engineering functions existed in `src/features.py`, there was no documented workflow showing how to apply them to the raw data and prepare datasets for modeling.

**Solution/Implementation**: Created `notebooks/02_Feature_Engineering.ipynb` that demonstrates the complete preprocessing pipeline:
- Loads raw data using `load_and_clean_data()`
- Applies `perform_feature_engineering()` to create derived features like `TenureRatio` and `SatisfactionComposite`
- Uses `split_data()` for **stratified sampling** to maintain attrition rate consistency
- Saves processed datasets as Parquet files for efficient storage and schema preservation

**Rationale/Logic**: This notebook serves as both documentation and executable pipeline. The **stratified split** is critical