"""This is the main module."""

from api import init_api
from config.app_config import DEBUG, CORS_ORIGINS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logger import configure_logger, logger

# Create fast api with title and description
app = FastAPI(
    title="BaselHack Plan B API",
    description="API for BaselHack Plan B Application",
    version="1.0.0",
    debug=DEBUG,
    docs_url="/",
    redoc_url=None,
)

# Add cors policies
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure global logger for app
configure_logger(app, logger)

# Initialize api routes
init_api(app)
