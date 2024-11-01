"""This is the app config module."""

import os

# All app configs
HOST = os.environ.get("HOST", "localhost")
PORT = os.environ.get("PORT", "5000")
DEBUG = bool(int(os.environ.get("DEBUG", "0")))

# All log configs
LOG_LEVELS = ["DEBUG", "INFO", "WARN", "WARNING", "ERROR", "FATAL", "CRITICAL"]
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Allowed CORS origins
CORS_ORIGINS = [
    "*",
]
