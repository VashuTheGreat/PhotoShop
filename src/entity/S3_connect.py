



import boto3
from src.constants import S3_CLIENT
from src.utils.asyncHandler import asyncHandler
from src.constants import SAVED_MODELS_FOLDER_PATH
import logging
import io
import os
class S3:
    def __init__(self,bucket_name:str):
        self.bucket_name=bucket_name
        self.s3=boto3.client(S3_CLIENT)
    
    @asyncHandler
    async def upload(self,file_path:str,s3_key:str):
        logging.info(f"uploading file to s3 {file_path} {s3_key}")
        self.s3.upload_file(file_path,self.bucket_name,s3_key)
        logging.info(f"uploaded file to s3 {file_path} {s3_key}")

    @asyncHandler
    async def loader(self,s3_key:str,loader_fn:object):
        file_path=os.path.join(SAVED_MODELS_FOLDER_PATH,s3_key)
        if not os.path.exists(file_path):
            os.makedirs(SAVED_MODELS_FOLDER_PATH, exist_ok=True)
            logging.info(f"Downloading {s3_key} from S3 bucket {self.bucket_name} to {file_path}")
            self.s3.download_file(self.bucket_name, s3_key, file_path)

        obj=loader_fn(file_path)
        return obj


