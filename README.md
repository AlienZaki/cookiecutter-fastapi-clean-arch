# Cookiecutter FastAPI Clean Architecture Template

A Cookiecutter template for creating FastAPI applications with clean architecture principles.

## Features

- **Clean Architecture**: Separation of concerns with domain, repositories, services, and API layers
- **Framework-Agnostic Domain**: Domain models use Python dataclasses (not Pydantic)
- **Dependency Injection**: Container pattern with lifecycle management
- **Protocol-Based Design**: Extensible architecture using Python protocols
- **Type Safety**: Strict pyright configuration
- **Modern Tooling**: `uv`, `ruff`, `pytest`, `pre-commit` hooks
- **Error Handling**: Domain exceptions mapped to HTTP status codes
- **Example Endpoints**: Included to demonstrate patterns

## Usage

### Install Cookiecutter

```bash
pip install cookiecutter
```

### Generate a New Project

```bash
cookiecutter cookiecutter-fastapi-clean-arch
```

You'll be prompted for:
- `project_name`: Name of your project
- `python_version`: Python version (default: 3.13)
- `description`: Project description
- `author_name`: Your name
- `author_email`: Your email
- `include_memory_repository`: Include in-memory repository (yes/no)
- `api_prefix`: API prefix (default: /api/v1)

### Example

```bash
cookiecutter cookiecutter-fastapi-clean-arch

project_name [My FastAPI Project]: My API Project
python_version [3.13]: 3.13
description [A FastAPI application with clean architecture]: A REST API with clean architecture
author_name [Your Name]: John Doe
author_email [your.email@example.com]: john@example.com
include_memory_repository [yes]: yes
api_prefix [/api/v1]: /api/v1
```

## Generated Project Structure

```
project_name/
├── app/
│   ├── core/           # Configuration, container (DI), logging
│   ├── domain/         # Framework-agnostic domain models (dataclasses) and protocols
│   ├── schemas/        # API request/response schemas (Pydantic)
│   ├── services/       # Business logic
│   ├── repositories/   # Data persistence implementations
│   └── api/            # FastAPI routes and error handlers
├── tests/
│   ├── unit/           # Unit tests (domain, services, repositories, api)
│   ├── integration/    # Integration tests
│   └── fixtures/       # Test fixtures
├── main.py             # Application entry point
├── pyproject.toml      # Project configuration
├── Makefile            # Common tasks
└── README.md           # Project documentation
```

## Getting Started

After generating your project:

1. **Create your domain models** in `app/domain/models.py` using Python dataclasses
2. **Create your schemas** in `app/schemas/` for API request/response serialization using Pydantic
3. **Implement your services** in `app/services/` with your business logic
4. **Update the container** in `app/core/container.py` to wire up your dependencies
5. **Create API endpoints** in `app/api/v1/endpoints/` and include them in `app/api/router.py`
6. **Register error handlers** in `app/api/error_handlers.py` for your domain exceptions
7. **Configure environment** by creating a `.env` file
8. **Run the application**: `make run`

The template may include example endpoints to demonstrate the architecture patterns. You can use them as a reference.

## Architecture Highlights

### Framework-Agnostic Domain Layer

Domain models use Python dataclasses instead of Pydantic, keeping the core domain independent of web framework concerns. Pydantic is only used in the API/schemas layer for request/response validation.

### Dependency Injection Container

The application uses a container pattern with lifecycle management:
- Lazy initialization of dependencies
- Factory pattern for creating repositories
- Lifecycle management integrated with FastAPI's lifespan events
- Easy to swap implementations (e.g., memory → database)

### Protocol-Based Design

Implement the `Repository` protocol for new storage backends. The container pattern makes it easy to swap implementations without changing business logic.

## License

This template is provided as-is. Feel free to modify and use as needed.
