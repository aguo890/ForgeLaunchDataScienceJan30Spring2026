# Forge Launch Spring 2026 — Data Science Track

A comprehensive submission for the Forge Launch Data Science Skills Challenge, demonstrating proficiency in **data analysis**, **machine learning**, **statistical modeling**, and **clean code practices**.

---

## 📁 Repository Structure

```
ForgeLaunchDataScienceJan30Spring2026/
├── src/                    # Core implementations
│   ├── analysis/           # Data analysis modules
│   ├── models/             # ML model implementations
│   └── utils/              # Utility functions
├── notebooks/              # Jupyter notebooks
│   ├── exploratory/        # EDA notebooks
│   └── final/              # Polished analysis notebooks
├── data/                   # Data files
│   ├── raw/                # Original, immutable data
│   ├── processed/          # Cleaned, transformed data
│   └── external/           # External reference data
├── test/                   # Unit tests & validation
├── docs/                   # Strategy docs, essays, reports
├── submission/             # Final deliverables
├── scripts/                # Automation utilities
├── Makefile                # Task runner
├── requirements.txt        # Python dependencies
└── STRATEGY_ANALYSIS.md    # Deep-dive technical analysis
```

---

## 🚀 Quick Start

### Requirements
| Tool      | Version   |
|-----------|-----------|
| Python    | v3.11+    |
| pip       | Latest    |
| Make      | (optional)|

### Setup
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Unix/MacOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run Tests
```bash
make test                          # Runs all unit tests via pytest
pytest test/                       # Direct command (no Make)
```

---

## 📂 Directory Guide

### `src/` — Core Implementations

| Directory | Description |
|-----------|-------------|
| **`analysis/`** | Data analysis modules (EDA, feature engineering, statistical tests) |
| **`models/`** | Machine learning model implementations |
| **`utils/`** | Utility functions (data loading, preprocessing, visualization helpers) |

### `notebooks/` — Jupyter Notebooks

| Directory | Purpose |
|-----------|---------|
| **`exploratory/`** | Rough exploration, hypothesis testing, prototyping |
| **`final/`** | Clean, presentation-ready analysis notebooks |

### `data/` — Data Storage

| Directory | Purpose |
|-----------|---------|
| **`raw/`** | Original data (never modify) |
| **`processed/`** | Cleaned and transformed data |
| **`external/`** | External reference datasets |

### `test/` — Test Suite

| File Pattern | Purpose |
|--------------|---------|
| **`test_*.py`** | Unit tests for source modules |
| **`conftest.py`** | Pytest fixtures and configuration |

### `docs/` — Documentation

| File | Description |
|------|-------------|
| **`analysis_strategy.md`** | Technical approach to data analysis |
| **`model_strategy.md`** | ML model selection and evaluation rationale |
| **`essays.md`** | Short essays (personal story + internship goals) |
| **`qa_report.md`** | QA verification report with test logs |
| **`development_log.md`** | Iteration history and decision changelog |

### `submission/` — Final Deliverables

| File | Description |
|------|-------------|
| **`MASTER_SUBMISSION.txt`** | Plain-text submission for copy-paste delivery |
| **`SUBMISSION_PREVIEW.md`** | Formatted markdown preview of final submission |

### `scripts/` — Automation

| Script | Command | Description |
|--------|---------|-------------|
| **`autocommit.py`** | `make push` | AI-powered git commit message generation |
| **`update_docs.py`** | `make docs` | AI-assisted documentation updates |
| **`validate_data.py`** | `make validate` | Data quality validation checks |

---

## 🔧 Makefile Commands

| Command | Description |
|---------|-------------|
| `make test` | Run all unit tests |
| `make lint` | Run code quality checks (flake8, black) |
| `make docs` | Update strategy documentation via AI |
| `make push` | Auto-commit with AI-generated message |
| `make smart-push` | Run `docs` then `push` sequentially |
| `make validate` | Run data validation checks |
| `make notebook` | Launch Jupyter Lab |
| `make clean` | Remove cached files and build artifacts |

---

## ✅ Implementation Checklist

- [ ] **Data Ingestion:** Load and validate raw data
- [ ] **Exploratory Data Analysis:** Comprehensive EDA notebook
- [ ] **Feature Engineering:** Transform raw features into model-ready inputs
- [ ] **Model Development:** Build and evaluate ML models
- [ ] **Model Validation:** Cross-validation and performance metrics
- [ ] **Documentation:** Strategy docs and technical write-ups
- [ ] **Essays:** Personal narrative + internship goals

---

## 🔗 Key Files for Reviewers

| What You're Looking For | Where to Find It |
|-------------------------|------------------|
| Data analysis modules | [`src/analysis/`](./src/analysis/) |
| ML implementations | [`src/models/`](./src/models/) |
| All tests passing | Run `make test` |
| EDA notebook | [`notebooks/exploratory/`](./notebooks/exploratory/) |
| Written essays | [`docs/essays.md`](./docs/essays.md) |
| QA proof of correctness | [`docs/qa_report.md`](./docs/qa_report.md) |
| Final submission text | [`submission/MASTER_SUBMISSION.txt`](./submission/MASTER_SUBMISSION.txt) |
| Technical strategy | [`STRATEGY_ANALYSIS.md`](./STRATEGY_ANALYSIS.md) |

---

## 📖 Further Reading

- **[`STRATEGY_ANALYSIS.md`](./STRATEGY_ANALYSIS.md)** — Deep-dive into data science philosophy, model selection, and analytical decisions.
- **[`docs/development_log.md`](./docs/development_log.md)** — Full changelog of iterations and refinements.
