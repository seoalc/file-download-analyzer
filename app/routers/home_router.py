from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.services.api_client import download_all_files, read_downloaded_files, calculate_statistics

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

@router.post("/calculate")
async def calculate(request: Request):
    form = await request.form()

    selected_files = form.getlist("selected_files")

    stats = calculate_statistics(selected_files)

    return templates.TemplateResponse(
        request=request,
        name="files.html",
        context={
            "request": request,
            "stats": stats
        }
    )

@router.post("/calculate-all")
async def calculate_all(request: Request):
    files = read_downloaded_files()

    selected_files = [
        file["file_name"]
        for file in files["files"]
    ]

    stats = calculate_statistics(selected_files)

    return templates.TemplateResponse(
        request=request,
        name="files.html",
        context={
            "request": request,
            "stats": stats
        }
    )