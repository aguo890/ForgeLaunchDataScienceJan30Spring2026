PYTHON_CMD ?= python
PIP_CMD ?= pip

# Argument handler for 'branch'
ifeq (branch,$(firstword $(MAKECMDGOALS)))
  BRANCH_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(BRANCH_ARGS):;@:)
endif

.PHONY: push branch test docs smart-push lint clean notebook validate setup

# Initial setup
setup:
	@echo "📦 Setting up environment..."
	@$(PIP_CMD) install -r requirements.txt

# Run all tests
test:
	@echo "🧪 Running all tests..."
	@$(PYTHON_CMD) -m pytest test/ -v --tb=short

# Run linting and formatting checks
lint:
	@echo "🔍 Running code quality checks..."
	@$(PYTHON_CMD) -m flake8 src/ test/ --max-line-length=120 --ignore=E501,W503
	@$(PYTHON_CMD) -m black src/ test/ --check

# Format code
format:
	@echo "✨ Formatting code..."
	@$(PYTHON_CMD) -m black src/ test/
	@$(PYTHON_CMD) -m isort src/ test/

# Update documentation using AI
docs:
	@echo "📚 Updating documentation..."
	@$(PYTHON_CMD) scripts/update_docs.py

# Push to GitHub (Auto-commit with AI)
push:
	@echo "🚀 Running push..."
	@$(PYTHON_CMD) scripts/autocommit.py

# Update docs and then push
smart-push: docs push

# Create a new branch
branch:
	@if "$(BRANCH_ARGS)"=="" (echo "⚠️  Usage: make branch <name>" & exit /b 1)
	@echo "🌿 Creating branch: $(BRANCH_ARGS)"
	@git checkout -b $(BRANCH_ARGS)
	@git push --set-upstream origin $(BRANCH_ARGS)

# Validate data quality
validate:
	@echo "📊 Running data validation..."
	@$(PYTHON_CMD) scripts/validate_data.py

# Launch Jupyter Lab
notebook:
	@echo "📓 Launching Jupyter Lab..."
	@$(PYTHON_CMD) -m jupyter lab

# Clean cached files
clean:
	@echo "🧹 Cleaning cached files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Clean complete!"
