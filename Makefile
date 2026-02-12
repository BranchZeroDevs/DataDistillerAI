.PHONY: help install install-dev setup test lint format clean run verify docker-up docker-down

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install -r requirements.txt
	python -m spacy download en_core_web_sm

install-dev:  ## Install development dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	python -m spacy download en_core_web_sm
	pre-commit install

setup: install-dev  ## Complete development setup
	@echo "✅ Development environment ready!"
	@echo "Run 'make verify' to check installation"

verify:  ## Verify installation
	python verify_installation.py

test:  ## Run tests
	pytest tests/ -v --tb=short

test-cov:  ## Run tests with coverage
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

lint:  ## Run linters
	flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 src/ --count --exit-zero --max-complexity=10 --max-line-length=100 --statistics

format:  ## Format code with black and isort
	black src/ examples/ --line-length=100
	isort src/ examples/ --profile=black

format-check:  ## Check code formatting
	black src/ examples/ --check --line-length=100
	isort src/ examples/ --check-only --profile=black

clean:  ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/ dist/ htmlcov/ .coverage

run:  ## Run the Streamlit app
	streamlit run app.py

quickstart:  ## Run quickstart example
	python examples/quickstart.py

docker-up:  ## Start Docker services (V2)
	docker compose up -d

docker-down:  ## Stop Docker services (V2)
	docker compose down

docker-logs:  ## View Docker logs
	docker compose logs -f

ci:  ## Run CI checks locally
	@echo "Running CI checks..."
	@make format-check
	@make lint
	@make test
	@echo "✅ All CI checks passed!"

all: clean install-dev lint test  ## Clean, install, lint, and test
