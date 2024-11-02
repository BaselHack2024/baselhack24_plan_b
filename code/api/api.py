"""This is the api module."""

from fastapi import APIRouter, FastAPI
from namespace import namespace

def init_api(app: FastAPI):
    """Initialize fast api app.

    This function initializes a fast api app
    and adds to it all necessary routes.

    Args:
        app : FastAPI
            An instance of a fast api app
    """
    # Creater API router with prefix
    api_v1 = APIRouter(prefix="/api")
    # Add all namespaces to API router
    api_v1.include_router(namespace)
    # Include API router in fast api app instance
    app.include_router(api_v1)
