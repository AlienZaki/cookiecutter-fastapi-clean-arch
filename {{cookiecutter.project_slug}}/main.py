import logging
import uvicorn

from app.api.router import app
from app.core.config import settings


def main() -> None:
    """Run the FastAPI application."""
    log_level = logging.DEBUG if settings.debug else logging.INFO
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level=logging.getLevelName(log_level).lower(),
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
