import os
import sys
from fastapi import FastAPI,Request
from fastapi.responses import StreamingResponse
import uvicorn as uv

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.routes.Emoji_router import router as emojiRouter
from src.routes.Bg_router import router as bgRouter
from src.routes.pages import router as htmlpagesRouter


sys.path.append(os.getcwd())

from src.logger import logging

app = FastAPI(title="PhotoShop ML API")




# --------- Templates ----------------

app.include_router(prefix="",router=htmlpagesRouter)



# --------- Modules -------------------------
app.include_router(prefix="/api/emoji",router=emojiRouter)
app.include_router(prefix="/api/bg",router=bgRouter)
