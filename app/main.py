"""BauDok - FastAPI Application Entry Point."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings

# API Routers
from app.routers import dashboard as dashboard_api
from app.routers import kunden as kunden_api
from app.routers import projekte as projekte_api

# View Routers (HTML)
from app.views import home as home_views
from app.views import kunden_views
from app.views import projekte_views

BASE_DIR = Path(__file__).parent


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        description="Dokumentenautomatisierung fuer Bauunternehmen",
        version="0.1.0",
        debug=settings.app_debug,
    )

    # Mount static files
    app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

    # Register API routers
    app.include_router(kunden_api.router)
    app.include_router(projekte_api.router)
    app.include_router(dashboard_api.router)

    # Register view routers (HTML pages)
    app.include_router(home_views.router)
    app.include_router(kunden_views.router)
    app.include_router(projekte_views.router)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_debug,
    )
