import logging
from logging import Logger


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: int = logging.INFO) -> None:
    """Configure application wide logging."""
    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[logging.StreamHandler()],
    )


def get_logger(name: str) -> Logger:
    """Return a logger for the given module."""
    return logging.getLogger(name)

