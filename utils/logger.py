# utils/logger.py
import logging


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
