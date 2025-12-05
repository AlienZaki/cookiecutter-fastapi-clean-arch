# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Requirements and Setup

- Python {{ cookiecutter.python_version }}
- uv
- Make

### Configuration

Create a `.env` file in the project root:

Available environment variables:
- `DEBUG`: Enable debug mode (default: `false`). When enabled, FastAPI runs in debug mode and uvicorn enables auto-reload.
- `LOG_LEVEL`: Logging level as integer (default: `20` for INFO). Common values: `10` (DEBUG), `20` (INFO), `30` (WARNING), `40` (ERROR), `50` (CRITICAL)

## How to Install and Run

Install dependencies (includes dev dependencies and pre-commit hooks):
```bash
make install
```

For production installations (without dev dependencies):
```bash
make install-prod
```

Start the FastAPI server:

```bash
make run
```

The API will be available at `http://localhost:8000`.

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check

The template may includes example endpoints to demonstrate the architecture. You can use them as a reference when creating your own endpoints.

## How to Run Tests

Run all tests
```bash
make test
```

or run specific test suite
```bash
uv run pytest tests/unit/
uv run pytest tests/integration/
```

## Pre-commit Hooks

Pre-commit hooks are automatically installed when you run `make install`. They run code quality checks before each commit and check:
- Code formatting (ruff)
- Type checking (pyright)
- Linting (ruff)
- File formatting (trailing whitespace, end of file, etc.)

You can also run hooks manually:
```bash
uv run pre-commit run --all-files
```

To update hooks to their latest versions:
```bash
uv run pre-commit autoupdate
```

## Project Structure

The codebase follows a clean architecture with clear separation of concerns:

- `domain/` - Defines framework-agnostic domain models (using dataclasses) and protocols (Repository, etc.)
- `repositories/` - Provides storage implementations (memory repository)
- `services/` - Orchestrates business logic
- `api/` - Exposes REST endpoints
- `schemas/` - Handles API request/response serialization (using Pydantic)
- `core/` - Configuration, container (dependency injection), and logging

## Getting Started

To get started, create your domain models and endpoints:

1. **Create your domain models** in `app/domain/models.py` using dataclasses (framework-agnostic)
2. **Create your schemas** in `app/schemas/` for API request/response serialization using Pydantic
3. **Implement your services** in `app/services/` with your business logic
4. **Create API endpoints** in `app/api/v1/endpoints/` and include them in `app/api/router.py`
5. **Update the container** in `app/core/container.py` to wire up your dependencies

## Architecture Highlights

### Framework-Agnostic Domain Layer

Domain models use Python dataclasses (not Pydantic), keeping the core domain independent of web framework concerns. Pydantic is only used in the API/schemas layer for request/response validation.

### Dependency Injection Container

The application uses a container pattern with lifecycle management:
- Lazy initialization of dependencies
- Factory pattern for creating repositories
- Lifecycle management integrated with FastAPI's lifespan events
- Easy to swap implementations (e.g., memory → database)

### Protocol-Based Design

The application uses protocol-based design allowing easy extension:

- Implement the `Repository` protocol for new storage backends (e.g., database)
- Configuration is environment-based and type-safe using Pydantic settings

### Error Handling

Domain exceptions are handled at the API layer with proper HTTP status codes. Register your custom exception handlers in `app/api/error_handlers.py` and add them to `app/api/router.py`.
