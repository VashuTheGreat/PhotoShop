import fastapi

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request


router=fastapi.APIRouter()




templates = Jinja2Templates(directory="templates")

@router.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(
        name="home.html",
        context={"request": request}
    )

@router.get("/emoji")
async def emoji_page(request: Request):
    return templates.TemplateResponse(
        name="emoji.html",
        context={"request": request}
    )

@router.get("/bg")
async def bg_page(request: Request):
    return templates.TemplateResponse(
        name="bg.html",
        context={"request": request}
    )
