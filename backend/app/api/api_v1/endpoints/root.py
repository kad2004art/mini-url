from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from redis import exceptions as dbExceptions

router = APIRouter

templates = Jinja2Templates(directory = frontent/templates)


@router.get("/", response_class = HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(name = "index.html", context = {"request": request})