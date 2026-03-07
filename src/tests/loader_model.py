
import asyncio
import sys
import os
sys.path.append(os.getcwd())
from src.logger import *
from src.entity.S3_connect import S3
from src.constants import BUCKET_NAME
from src.utils.loader_functions import EmojiFaceGenerator,BgRemover
uploader=S3(bucket_name=BUCKET_NAME)



# print(asyncio.run(uploader.loader(s3_key="EmojiFaceGenerator.pth",loader_fn=EmojiFaceGenerator)))
# print(asyncio.run(uploader.loader(s3_key="BgRemover.pth",loader_fn=BgRemover)))