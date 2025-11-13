.PHONY: help install dev-install test coverage lint format clean run docker-build docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install       - Install production dependencies"
	@echo "  make dev-install   - Install development dependencies and pre-commit hooks"
	@echo "  make test          - Run tests"
	@echo "  make coverage      - Run tests with coverage report"
	@echo "  make lint          - Run linting checks"
	@echo "  make format        - Format code with black and isort"
	@echo "  make clean         - Clean up temporary files"
	@echo "  make run           - Run the application"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-up     - Start Docker containers"
	@echo "  make docker-down   - Stop Docker containers"

install:
	pip install -r requirements.txt

dev-install: install
	pip install pre-commit
	pre-commit install

test:
	pytest -v

coverage:
	pytest --cov=app --cov-report=html --cov-report=term

lint:
	black --check app/ tests/
	isort --check-only app/ tests/
	flake8 app/ tests/ --max-line-length=100 --extend-ignore=E203,W503
	mypy app/ --ignore-missing-imports

format:
	black app/ tests/
	isort app/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -f .coverage
	rm -f *.db

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t todo-api .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down
