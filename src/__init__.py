from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import api_router


def init_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "https://checkibot.willypaz.dev"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router)
    return app
