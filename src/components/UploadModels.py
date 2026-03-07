from src.utils.asyncHandler import asyncHandler
from src.entity.S3_connect import S3
from src.constants import BUCKET_NAME
class UploadModels:
    def __init__(self):
        self.s3=S3(bucket_name=BUCKET_NAME)

    @asyncHandler
    async def UploadModel(self,file_path:str,s3_key:str):
        await self.s3.upload(file_path=file_path,s3_key=s3_key)
            
        