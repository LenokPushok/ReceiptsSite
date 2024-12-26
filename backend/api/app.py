from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import routers
from api.settings import app_settings


def create_app():
    app = FastAPI(**app_settings.model_dump())

    app.add_middleware(
        CORSMiddleware,  # noqa
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for router in routers:
        app.include_router(router)
    return app
