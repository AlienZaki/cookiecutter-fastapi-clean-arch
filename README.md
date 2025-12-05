# Cookiecutter FastAPI Clean Architecture Template

A Cookiecutter template for creating FastAPI applications with clean architecture principles.

## Features

- **Clean Architecture**: Separation of concerns with domain, repositories, services, and API layers
- **Protocol-Based Design**: Extensible architecture using Python protocols
- **Type Safety**: Strict pyright configuration for type checking
- **Testing**: Comprehensive test structure with unit and integration tests
- **Modern Tooling**: Uses `uv` for dependency management, `ruff` for linting
- **Flexible Storage**: Support for memory and JSON file repositories
- **Modular**: `modules/` directory for custom functionality
- **Clean Starting Point**: Empty structure ready for your domain models

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

project_name [My FastAPI Project]: Product Catalog API
python_version [3.13]: 3.13
description [A FastAPI application with clean architecture]: A product catalog API
author_name [Your Name]: John Doe
author_email [your.email@example.com]: john@example.com
include_memory_repository [yes]: yes
api_prefix [/api/v1]: /api/v1
```

## Generated Project Structure

```
project_name/
├── app/
│   ├── core/           # Configuration
│   ├── domain/         # Domain models and protocols
│   ├── schemas/        # API request/response schemas
│   ├── services/       # Business logic
│   ├── repositories/   # Data persistence
│   ├── api/            # FastAPI routes
│   └── modules/        # Custom modules (scrapers, processors, etc.)
├── tests/
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── fixtures/       # Test fixtures
├── data/               # Data directory
├── main.py             # Application entry point
├── pyproject.toml      # Project configuration
├── Makefile            # Common tasks
└── README.md           # Project documentation
```

## Getting Started

After generating your project:

1. **Create your domain models** in `app/domain/models.py`
2. **Create your schemas** in `app/schemas/` for API request/response serialization
3. **Implement your services** in `app/services/` with your business logic
4. **Add custom modules** in `app/modules/`
5. **Create API endpoints** in `app/api/v1/endpoints/` and include them in `app/api/router.py`
6. **Configure environment** by creating a `.env` file
7. **Run the application**: `make run`

## Development

The template generates a project with:
- FastAPI for the web framework
- Pydantic for data validation
- pytest for testing
- pyright for type checking
- ruff for linting
- uv for dependency management

## License

This template is provided as-is. Feel free to modify and use as needed.
