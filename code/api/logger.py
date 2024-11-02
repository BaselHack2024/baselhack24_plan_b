"""This is the logger module."""

import logging
import sys

import loguru
from config.app_config import LOG_LEVEL, LOG_LEVELS
from fastapi import FastAPI
from loguru import logger

# Define loguru logger
logger: loguru.logger = logger  # noqa: F811
# Remove default python logger
logger.remove()


def configure_logger(app: FastAPI, logger_instance: loguru.logger):
    """Configure global logger.

    Args:
        app : FastAPI
            Instance of fast api
        logger_instance : loguru.logger
            Logger instance that should be configured
    """
    log_level = LOG_LEVEL
    # Check if log level is in possible log levels
    if log_level in LOG_LEVELS:
        # Set textual or numeric representation of logging level
        log_level = logging.getLevelName(log_level)

    # Check if app is in debug
    if app.debug:
        # Set debug level
        log_level = logging.DEBUG

    # Add to logger instance log configuration
    logger_instance.add(
        sys.stdout,
        colorize=True,
        diagnose=app.debug,
        level=logging.getLevelName(log_level),
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green>"
        + " | {level} | <level>{message}</level>",
    )
