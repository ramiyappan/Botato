import logging
import sys
import os

os.makedirs("logs", exist_ok=True)

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # Console handler
        stream_formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )

        # File handler
        file_handler = logging.FileHandler("logs/app.log")
        file_handler.setFormatter(stream_formatter)
        logger.addHandler(file_handler)

    return logger
