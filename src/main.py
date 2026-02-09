from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_config
from src.api.routes import translate, health


def create_app() -> FastAPI:
    """Application factory."""
    config = get_config()

    app = FastAPI(
        title=config.APP_NAME,
        debug=config.DEBUG,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(health.router, tags=["Health"])
    app.include_router(translate.router, tags=["Translation"])

    return app

app = create_app()
