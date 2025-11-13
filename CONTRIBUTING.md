# Contributing to Todo API

Thank you for your interest in contributing to the Todo API project! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow. Please be respectful and professional in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/Todos-FAST-APIs-Backend.git
   cd Todos-FAST-APIs-Backend
   ```
3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/pyenthusiasts/Todos-FAST-APIs-Backend.git
   ```

## Development Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install development dependencies**:
   ```bash
   make dev-install
   # or manually:
   pip install -r requirements.txt
   pip install pre-commit
   pre-commit install
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

## Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   # or for bug fixes:
   git checkout -b fix/bug-description
   ```

2. **Make your changes**:
   - Write code following the coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests**:
   ```bash
   make test
   ```

4. **Check code quality**:
   ```bash
   make lint
   ```

5. **Format code**:
   ```bash
   make format
   ```

6. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Your descriptive commit message"
   ```

7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Open a Pull Request** on GitHub

## Coding Standards

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use **Black** for code formatting (line length: 100)
- Use **isort** for import sorting
- Use **type hints** where appropriate
- Write **docstrings** for all functions, classes, and modules

### Code Organization

- Keep functions small and focused
- Follow the Single Responsibility Principle
- Use meaningful variable and function names
- Avoid magic numbers; use named constants

### Example Code Style

```python
"""Module for handling todo operations."""
from typing import List, Optional
from sqlalchemy.orm import Session


def get_all_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Todo]:
    """
    Retrieve all todos from the database.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of Todo objects
    """
    return db.query(Todo).offset(skip).limit(limit).all()
```

## Testing Guidelines

### Writing Tests

- Write tests for all new features and bug fixes
- Maintain test coverage above 80%
- Use descriptive test names that explain what is being tested
- Follow the Arrange-Act-Assert pattern

### Test Structure

```python
def test_create_todo(client):
    """Test creating a new todo."""
    # Arrange
    todo_data = {
        "title": "Test Todo",
        "description": "Test description",
        "completed": False
    }

    # Act
    response = client.post("/api/v1/todos", json=todo_data)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == todo_data["title"]
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make coverage

# Run specific test file
pytest tests/test_todos.py

# Run specific test
pytest tests/test_todos.py::test_create_todo
```

## Commit Messages

Write clear and meaningful commit messages following these guidelines:

### Format

```
<type>: <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```
feat: Add pagination support to todo list endpoint

- Add skip and limit query parameters
- Update tests to cover pagination
- Update API documentation

Closes #123
```

```
fix: Resolve database connection issue

- Fix connection pool configuration
- Add retry logic for transient errors

Fixes #456
```

## Pull Request Process

1. **Update documentation** for any changed functionality
2. **Add tests** for new features or bug fixes
3. **Ensure all tests pass** locally
4. **Run code quality checks** (lint, format)
5. **Update the README** if needed
6. **Submit the pull request** with a clear description

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Description of testing performed

## Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No new warnings
```

### Review Process

- At least one maintainer will review your PR
- Address any feedback or requested changes
- Once approved, a maintainer will merge your PR

## Questions?

If you have questions or need help, please:
- Open an issue on GitHub
- Check existing documentation
- Review closed issues for similar questions

Thank you for contributing to the Todo API project!
