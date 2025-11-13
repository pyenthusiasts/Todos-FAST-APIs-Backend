# Architecture Documentation

## Overview

This document describes the architecture and design decisions of the Todo API application.

## Architecture Style

The application follows a **Layered Architecture** pattern with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│          API Layer (FastAPI)            │
│    Routes, Request/Response Handling    │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         Service Layer (Business)        │
│      Business Logic, Validation         │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│       Data Access Layer (ORM)           │
│    Database Operations, Transactions    │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          Database (SQLite/PostgreSQL)   │
└─────────────────────────────────────────┘
```

## Directory Structure

```
app/
├── api/              # API routes and endpoints
├── core/             # Core application configuration
├── db/               # Database configuration
├── middleware/       # Custom middleware
├── models/           # SQLAlchemy ORM models
├── schemas/          # Pydantic validation schemas
└── services/         # Business logic layer
```

## Components

### 1. API Layer (`app/api/`)

**Responsibility**: Handle HTTP requests and responses

**Key Files**:
- `todos.py` - Todo CRUD endpoints
- `health.py` - Health check endpoints

**Design Decisions**:
- Uses FastAPI's dependency injection for database sessions
- Implements API versioning (`/api/v1/`)
- Returns Pydantic models for type safety
- Proper HTTP status codes

### 2. Service Layer (`app/services/`)

**Responsibility**: Business logic and operations

**Key Files**:
- `todo_service.py` - Todo business operations

**Design Decisions**:
- Stateless service classes
- Pure functions where possible
- Transaction management
- Encapsulates complex business rules

### 3. Data Access Layer (`app/models/`, `app/db/`)

**Responsibility**: Database operations

**Key Files**:
- `models/todo.py` - Todo ORM model
- `db/database.py` - Database configuration

**Design Decisions**:
- SQLAlchemy ORM for database abstraction
- Alembic for migrations
- Connection pooling
- Automatic timestamps

### 4. Schemas Layer (`app/schemas/`)

**Responsibility**: Data validation and serialization

**Key Files**:
- `schemas/todo.py` - Todo Pydantic models

**Design Decisions**:
- Separate schemas for create/update/response
- Type hints for IDE support
- Field validation rules
- Documentation strings

### 5. Middleware (`app/middleware/`)

**Responsibility**: Cross-cutting concerns

**Middleware Stack** (order matters):
1. `RateLimitMiddleware` - Rate limiting
2. `SecurityHeadersMiddleware` - Security headers
3. `RequestIDMiddleware` - Request tracing
4. `LoggingMiddleware` - Request/response logging
5. `CORSMiddleware` - CORS handling

**Design Decisions**:
- Composable middleware
- Independent and reusable
- Minimal performance impact

### 6. Core (`app/core/`)

**Responsibility**: Application configuration and utilities

**Key Files**:
- `config.py` - Settings management
- `logging.py` - Logging configuration
- `exceptions.py` - Custom exceptions
- `exception_handlers.py` - Global error handling

## Data Flow

### Request Flow

```
1. HTTP Request
        ↓
2. Middleware Stack (CORS → Logging → RequestID → Security → RateLimit)
        ↓
3. Route Handler (API Layer)
        ↓
4. Input Validation (Pydantic Schema)
        ↓
5. Service Layer (Business Logic)
        ↓
6. Data Access Layer (ORM)
        ↓
7. Database
        ↓
8. Response (Pydantic Schema)
        ↓
9. Middleware Stack (reverse order)
        ↓
10. HTTP Response
```

### Error Flow

```
1. Exception Raised
        ↓
2. Exception Handler
        ↓
3. Error Logging
        ↓
4. Structured Error Response
        ↓
5. HTTP Error Status
```

## Database Schema

### Todos Table

```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    CONSTRAINT pk_todos PRIMARY KEY (id)
);

CREATE INDEX ix_todos_id ON todos (id);
CREATE INDEX ix_todos_title ON todos (title);
```

## Design Patterns

### 1. Dependency Injection

```python
def get_todos(db: Session = Depends(get_db)):
    # Database session injected automatically
    return TodoService.get_all_todos(db)
```

**Benefits**:
- Loose coupling
- Easy testing
- Clear dependencies

### 2. Repository Pattern (Implicit)

Service layer acts as repositories:

```python
class TodoService:
    @staticmethod
    def get_todo_by_id(db: Session, todo_id: int):
        # Encapsulates data access
```

**Benefits**:
- Abstraction over data access
- Testable business logic
- Swappable data sources

### 3. Strategy Pattern (Middleware)

Different middleware strategies for cross-cutting concerns:

```python
app.add_middleware(RateLimitMiddleware, requests_per_minute=60)
app.add_middleware(SecurityHeadersMiddleware)
```

### 4. Factory Pattern (Database Sessions)

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Security Architecture

### Defense in Depth

Multiple security layers:

1. **Network**: HTTPS, firewall
2. **Application**: Rate limiting, input validation
3. **Database**: Parameterized queries, least privilege
4. **Monitoring**: Logging, alerting

### Security Headers

Implemented via `SecurityHeadersMiddleware`:
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection
- Strict-Transport-Security
- Content-Security-Policy

### Request Validation

```python
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
```

## Scalability Considerations

### Horizontal Scaling

- Stateless API design
- Database connection pooling
- Load balancer ready
- Session management (Redis for JWT)

### Vertical Scaling

- Efficient database queries
- Indexed columns
- Connection pooling
- Async operations support

### Caching Strategy (Future)

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Client  │ → → │  Redis   │ → → │ Database │
└──────────┘     └──────────┘     └──────────┘
                  (Cache Layer)
```

## Monitoring and Observability

### Logging

- **Request Logging**: All requests/responses
- **Error Logging**: Stack traces, context
- **Business Logging**: Important operations

### Metrics

- Request count
- Response time
- Error rate
- Database connection pool

### Tracing

- Request ID tracking
- Distributed tracing ready
- Correlation IDs

## Testing Strategy

### Test Pyramid

```
        ╱╲
       ╱  ╲      Unit Tests (70%)
      ╱────╲
     ╱      ╲    Integration Tests (20%)
    ╱────────╲
   ╱          ╲  E2E Tests (10%)
  ╱────────────╲
```

### Test Types

1. **Unit Tests**: Service layer logic
2. **Integration Tests**: API endpoints with DB
3. **E2E Tests**: Full workflow tests

## Performance Optimization

### Database

- Indexes on frequently queried columns
- Connection pooling
- Query optimization
- Batch operations

### Application

- Async operations
- Efficient middleware
- Response compression
- Static file caching

### Network

- HTTP/2 support
- Keep-alive connections
- CDN for static assets

## Deployment Architecture

### Production Setup

```
┌─────────────┐
│ Load        │
│ Balancer    │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
┌──▼───┐ ┌▼────┐
│ App  │ │ App │
│ Node │ │ Node│
└──┬───┘ └┬────┘
   │      │
   └──┬───┘
      │
┌─────▼─────┐
│ Database  │
│ (Primary) │
└───────────┘
      │
┌─────▼─────┐
│ Database  │
│ (Replica) │
└───────────┘
```

## Future Enhancements

### Planned Features

1. **Authentication & Authorization**
   - JWT tokens
   - Role-based access control
   - OAuth2 support

2. **Caching**
   - Redis integration
   - Response caching
   - Database query caching

3. **Background Tasks**
   - Celery integration
   - Scheduled tasks
   - Async operations

4. **WebSockets**
   - Real-time updates
   - Live notifications

5. **API Gateway**
   - Centralized authentication
   - Request routing
   - API composition

## Technology Stack

### Core Technologies

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM and database toolkit
- **Alembic**: Database migrations
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Supporting Tools

- **pytest**: Testing framework
- **Black**: Code formatter
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

## Best Practices

### Code Quality

- Type hints everywhere
- Docstrings for all functions
- PEP 8 compliance
- DRY principle

### Database

- Migrations for all schema changes
- Indexes on foreign keys
- Proper constraints
- Regular backups

### API Design

- RESTful conventions
- Versioning
- Consistent error responses
- Comprehensive documentation

### Security

- Input validation
- Output encoding
- Secure headers
- Rate limiting
- Regular updates

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [12-Factor App](https://12factor.net/)
