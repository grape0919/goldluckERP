from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles 

from starlette.exceptions import HTTPException

from router.view import view_router

# from db.database import engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static") 

# @app.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#     return templates.TemplateResponse("workspace/alert.html", {"request":request, "message":exc.detail})

app.include_router(view_router)
