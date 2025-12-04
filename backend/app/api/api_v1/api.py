from fastapi import APIRouter

from .endpoints import root, shortener

api_router = APIRouter()
api_router.include_router(root.router, tags = ["root"])
api_router.include_router(shortener.router, tags = ["shortener"])