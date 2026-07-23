from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.services.api_client import download_all_files, read_downloaded_files

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@router.post("/download")
async def download(request: Request):
    download_all_files()

    return RedirectResponse(
        url="/",
        status_code=303
    )

@router.get("/files", response_class=HTMLResponse)
async def files(request: Request):
    stats = read_downloaded_files()

    return templates.TemplateResponse(
        request=request,
        name="files.html",
        context={
            "request": request,
            "stats": stats
        }
    )