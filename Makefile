.PHONY: help install dev-install test coverage lint format clean run docker-build docker-up docker-down db-init db-migrate db-upgrade db-backup db-restore seed-data security-check

help:
	@echo "Available commands:"
	@echo ""
	@echo "Installation:"
	@echo "  make install       - Install production dependencies"
	@echo "  make dev-install   - Install development dependencies and pre-commit hooks"
	@echo ""
	@echo "Development:"
	@echo "  make run           - Run the application"
	@echo "  make format        - Format code with black and isort"
	@echo "  make lint          - Run linting checks"
	@echo "  make test          - Run tests"
	@echo "  make coverage      - Run tests with coverage report"
	@echo "  make clean         - Clean up temporary files"
	@echo ""
	@echo "Database:"
	@echo "  make db-init       - Initialize database"
	@echo "  make db-migrate    - Create new migration"
	@echo "  make db-upgrade    - Apply migrations"
	@echo "  make db-backup     - Backup database"
	@echo "  make seed-data     - Seed database with sample data"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-up     - Start Docker containers"
	@echo "  make docker-down   - Stop Docker containers"
	@echo ""
	@echo "Security:"
	@echo "  make security-check - Run security checks"

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

# Database commands
db-init:
	python scripts/init_db.py

db-migrate:
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

db-upgrade:
	alembic upgrade head

db-backup:
	python scripts/db_backup.py backup

db-restore:
	@read -p "Enter backup file path: " file; \
	python scripts/db_backup.py restore --file "$$file"

seed-data:
	python scripts/seed_data.py

# Security checks
security-check:
	@echo "Running security checks..."
	@pip install bandit safety 2>/dev/null || true
	@echo "\n=== Checking dependencies for vulnerabilities ==="
	@safety check || true
	@echo "\n=== Running Bandit security linter ==="
	@bandit -r app/ -ll || true
	@echo "\n=== Security check complete ==="
