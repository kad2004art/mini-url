from fastapi import FastAPI
from fastapi.staticfile import StaticFiles

from .api.api_v1.api import api_router
from .config import settings

app = FastAPI(title = settings.APP_NAME)
app.mount("/static", StaticFiles(directory = "frontend/static"), name = "static")
app.include_router(api_router)