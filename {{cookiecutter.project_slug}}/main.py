import uvicorn

from app.api.router import app
from app.core.config import settings


def main() -> None:
    """Run the FastAPI application."""
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level=settings.log_level if not settings.debug else "debug",
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
