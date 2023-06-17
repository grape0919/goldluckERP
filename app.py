from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles 

from starlette.exceptions import HTTPException

from router.view import view_router
from router.api import api_router
from router.auth import auth_router

from db import models
from db.database import engine

from router.view import templates

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static") 

@app.get("/favicon.ico") 
async def favicon(): 
	return FileResponse("favicon.png")

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return templates.TemplateResponse("workspace/alert.html", {"request":request, "message":exc.detail})



app.include_router(view_router)
app.include_router(api_router)
app.include_router(auth_router)
