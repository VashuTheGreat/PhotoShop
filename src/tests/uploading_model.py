
import asyncio
import sys
import os
sys.path.append(os.getcwd())
from src.logger import *
from src.components.UploadModels import UploadModels

uploader=UploadModels()

asyncio.run(uploader.UploadModel(file_path="models/BgRemover.pth",s3_key="BgRemover.pth"))
asyncio.run(uploader.UploadModel(file_path="models/EmojiFaceGenerator.pth",s3_key="EmojiFaceGenerator.pth"))
