from src.app import *
from src.logger import *
import uvicorn as uv
from dotenv import load_dotenv
load_dotenv()
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uv.run("main:app", host="0.0.0.0", port=8000, reload=True)
