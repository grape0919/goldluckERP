from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="templates") 

view_router = APIRouter(
    prefix="",
    tags=[""],
    responses={404: {"description": "Not found"}},
)

@view_router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})