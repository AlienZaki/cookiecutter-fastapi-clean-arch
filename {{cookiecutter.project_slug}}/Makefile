.PHONY: help install install-prod install-pre-commit test lint lint-fix type-check clean clean-all run

PYTHON := python
UV := uv
PYTEST := $(UV) run pytest
RUFF := $(UV) run ruff
PYRIGHT := $(UV) run pyright

.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install project dependencies including dev dependencies and pre-commit hooks (default for development)
	$(UV) sync --group dev
	@if git rev-parse --git-dir > /dev/null 2>&1; then \
		$(UV) run pre-commit install; \
	else \
		echo "Note: Skipping pre-commit install (not a git repository). Run 'make install-pre-commit' after initializing git."; \
	fi

install-prod: ## Install project dependencies for production (without dev dependencies)
	$(UV) sync --no-group dev

install-pre-commit: ## Install pre-commit hooks only
	$(UV) run pre-commit install

test: ## Run tests
	$(PYTEST) tests/

lint: ## Run linter (ruff check)
	$(RUFF) check .

lint-fix: ## Run linter and fix issues automatically
	$(RUFF) check --fix --unsafe-fixes .

type-check: ## Run type checker (pyright)
	$(PYRIGHT) .

run: ## Run the application
	$(UV) run python main.py

clean: ## Remove build artifacts and cache files
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".pyright" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -r {} + 2>/dev/null || true

clean-all: clean ## Remove build artifacts, cache files, and virtual environment
	rm -rf .venv 2>/dev/null || true

