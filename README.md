# Todo Application Backend with FastAPI

A production-ready, scalable REST API for managing todo items built with FastAPI, featuring a clean architecture, comprehensive testing, Docker support, and CI/CD integration.

[![CI/CD Pipeline](https://github.com/pyenthusiasts/Todos-FAST-APIs-Backend/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/pyenthusiasts/Todos-FAST-APIs-Backend/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Docker Deployment](#docker-deployment)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Development](#development)
- [CI/CD](#cicd)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Modern FastAPI Framework**: High-performance async API framework with automatic OpenAPI documentation
- **Clean Architecture**: Well-organized code structure with separation of concerns (models, schemas, services, routes)
- **Database Integration**: SQLAlchemy ORM with SQLite (easily configurable for PostgreSQL)
- **API Versioning**: Built-in API versioning support (`/api/v1/`)
- **Comprehensive Testing**: Full test suite with pytest, including unit and integration tests
- **Docker Support**: Complete Docker and Docker Compose configuration for easy deployment
- **CI/CD Pipeline**: GitHub Actions workflow for automated testing and deployment
- **Code Quality**: Pre-commit hooks with Black, isort, flake8, and mypy
- **Logging**: Structured JSON logging for production environments
- **Configuration Management**: Environment-based configuration using Pydantic settings
- **CORS Support**: Configurable CORS middleware for cross-origin requests
- **Health Checks**: Built-in health check endpoint for monitoring
- **Pagination**: Support for paginated results on list endpoints
- **Filtering**: Filter todos by status (completed/pending)

## Project Structure

```
Todos-FAST-APIs-Backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── todos.py           # Todo endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration settings
│   │   └── logging.py         # Logging configuration
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py        # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   └── todo.py            # SQLAlchemy models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── todo.py            # Pydantic schemas
│   ├── services/
│   │   ├── __init__.py
│   │   └── todo_service.py    # Business logic
│   ├── __init__.py
│   └── main.py                # Application entry point
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Test fixtures
│   ├── test_main.py           # Main app tests
│   └── test_todos.py          # Todo endpoint tests
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI/CD
├── .dockerignore
├── .env.example               # Environment variables template
├── .gitignore
├── .pre-commit-config.yaml    # Pre-commit hooks configuration
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Docker image definition
├── LICENSE
├── pyproject.toml             # Python project configuration
├── README.md
└── requirements.txt           # Python dependencies
```

## Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/pyenthusiasts/Todos-FAST-APIs-Backend.git
cd Todos-FAST-APIs-Backend

# Run with Docker Compose
docker-compose up --build

# API will be available at http://localhost:8000
```

### Manual Setup

```bash
# Clone the repository
git clone https://github.com/pyenthusiasts/Todos-FAST-APIs-Backend.git
cd Todos-FAST-APIs-Backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m uvicorn app.main:app --reload

# API will be available at http://localhost:8000
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Docker and Docker Compose (optional, for containerized deployment)
- Git

### Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pyenthusiasts/Todos-FAST-APIs-Backend.git
   cd Todos-FAST-APIs-Backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Install pre-commit hooks** (optional but recommended):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Configuration

Configuration is managed through environment variables. Copy `.env.example` to `.env` and customize as needed:

```bash
# API Configuration
API_V1_PREFIX=/api/v1
PROJECT_NAME=Todo API
VERSION=1.0.0

# Database Configuration
DATABASE_URL=sqlite:///./todos.db
# For PostgreSQL: postgresql://user:password@localhost/dbname

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Logging
LOG_LEVEL=INFO
```

### Database Configuration

**SQLite (Default)**:
```
DATABASE_URL=sqlite:///./todos.db
```

**PostgreSQL**:
```
DATABASE_URL=postgresql://username:password@localhost:5432/tododb
```

## Running the Application

### Development Mode

```bash
# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the main.py script
python -m app.main
```

### Production Mode

```bash
# Using uvicorn with workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Docker Deployment

### Build and Run with Docker

```bash
# Build the Docker image
docker build -t todo-api .

# Run the container
docker run -p 8000:8000 todo-api
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up --build
```

## API Documentation

Once the application is running, you can access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## API Endpoints

### Root Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint with API information |
| GET | `/health` | Health check endpoint |

### Todo Endpoints

All todo endpoints are prefixed with `/api/v1/todos`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/todos` | Get all todos (with pagination) |
| GET | `/api/v1/todos/completed` | Get all completed todos |
| GET | `/api/v1/todos/pending` | Get all pending todos |
| GET | `/api/v1/todos/{todo_id}` | Get a specific todo by ID |
| POST | `/api/v1/todos` | Create a new todo |
| PUT | `/api/v1/todos/{todo_id}` | Update a todo |
| DELETE | `/api/v1/todos/{todo_id}` | Delete a todo |

### Request Examples

**Create a Todo**:
```bash
curl -X POST "http://localhost:8000/api/v1/todos" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, Bread, Eggs",
    "completed": false
  }'
```

**Get All Todos with Pagination**:
```bash
curl -X GET "http://localhost:8000/api/v1/todos?skip=0&limit=10"
```

**Update a Todo**:
```bash
curl -X PUT "http://localhost:8000/api/v1/todos/1" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

**Delete a Todo**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/todos/1"
```

## Testing

### Run All Tests

```bash
# Run all tests with coverage
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_todos.py

# Run specific test
pytest tests/test_todos.py::TestTodoAPI::test_create_todo
```

### Test Coverage

View the coverage report:
```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html  # On macOS
```

## Development

### Code Quality Tools

The project uses several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

Run all checks:
```bash
# Format code
black app/ tests/

# Sort imports
isort app/ tests/

# Lint code
flake8 app/ tests/ --max-line-length=100

# Type check
mypy app/
```

### Pre-commit Hooks

Pre-commit hooks automatically run code quality checks before each commit:

```bash
# Install hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

### Database Migrations

For database schema changes, you can use Alembic:

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "Add new column"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## CI/CD

The project includes a GitHub Actions workflow that automatically:

1. Runs tests on multiple Python versions (3.9, 3.10, 3.11)
2. Checks code quality (Black, isort, flake8, mypy)
3. Builds Docker image
4. Generates test coverage reports
5. Tests the Docker container

The workflow runs on:
- Push to `main`, `develop`, or `claude/*` branches
- Pull requests to `main` or `develop` branches

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Run tests**: `pytest`
5. **Run code quality checks**: `pre-commit run --all-files`
6. **Commit your changes**: `git commit -m 'Add amazing feature'`
7. **Push to the branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Development Guidelines

- Write tests for new features
- Maintain test coverage above 80%
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Update documentation for API changes
- Keep commits atomic and well-described

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework for building APIs
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation using Python type hints
- [Uvicorn](https://www.uvicorn.org/) - Lightning-fast ASGI server

---

**Happy Coding!** If you have any questions or feedback, please open an issue or reach out to the maintainers.
