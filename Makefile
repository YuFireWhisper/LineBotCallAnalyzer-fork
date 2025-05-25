.PHONY: help install test test-unit test-integration run clean lint format

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -r requirements.txt

test:  ## Run all tests
	python run_tests.py --type all

test-unit:  ## Run unit tests only
	python run_tests.py --type unit

test-integration:  ## Run integration tests only
	python run_tests.py --type integration

test-pytest:  ## Run tests with pytest
	pytest

test-coverage:  ## Run tests with coverage report
	pytest --cov=app --cov-report=html --cov-report=term

run:  ## Run the application
	python run.py

clean:  ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.log" -delete
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/

lint:  ## Run linting
	flake8 app/ tests/ --max-line-length=100 --ignore=E203,W503

format:  ## Format code
	black app/ tests/ --line-length=100

check:  ## Run all checks (lint, format check, tests)
	black --check app/ tests/ --line-length=100
	flake8 app/ tests/ --max-line-length=100 --ignore=E203,W503
	python run_tests.py --type all
