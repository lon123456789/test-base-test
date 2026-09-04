import logging
import os


def setup_logger(name: str = "token_analyzer", level: str = "INFO") -> logging.Logger:
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level.upper())

    # File handler
    file_handler = logging.FileHandler(os.path.join(log_dir, f"{name}.log"))
    file_handler.setLevel(level.upper())

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level.upper())

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Avoid duplicate handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":
    log = setup_logger()
    log.info("Logger initialized.")
