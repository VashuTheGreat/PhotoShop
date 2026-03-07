import torch
import cv2
import io
import numpy as np
from PIL import Image

from src.utils.asyncHandler import asyncHandler
from src.entity.S3_connect import S3
from src.constants import BUCKET_NAME, BG_REMOVER_MODEL_NAME, DEVICE
from src.utils.loader_functions import BgRemover


class RemovedBackground:

    def __init__(self):
        self.s3 = S3(bucket_name=BUCKET_NAME)
        self.model = None


    def preprocess(self, image_path):

        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image = image / 255.0
        image = image.astype("float32")

        image = cv2.resize(image, (224, 224))

        tensor = torch.from_numpy(image).permute(2, 0, 1)
        tensor = tensor.unsqueeze(0)

        return tensor.to(DEVICE)


    def postprocess(self, mask):

        mask = mask.squeeze().cpu().numpy()
        mask = (mask * 255).astype("uint8")

        return mask


    async def remove_bg_by_segment(self, image_path, mask_array):
        # Load original image
        image = cv2.imread(image_path)
        if image is None:
            raise Exception(f"Could not read image at {image_path}")
            
        # Convert to BGRA (4 channels)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        
        # Resize mask to original image size
        mask_resized = cv2.resize(mask_array, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_LANCZOS4)
        
        # Optional: Threshold the mask to make it cleaner
        _, mask_binary = cv2.threshold(mask_resized, 127, 255, cv2.THRESH_BINARY)
        
        # Apply mask to alpha channel
        image[:, :, 3] = mask_binary
        
        # Encode to PNG buffer
        _, buffer = cv2.imencode(".png", image)
        io_buffer = io.BytesIO(buffer)
        io_buffer.seek(0)
        
        return io_buffer

    @asyncHandler
    async def _remove_background(self, image_path):
        if self.model is None:
            self.model = await self.s3.loader(
                s3_key=BG_REMOVER_MODEL_NAME,
                loader_fn=BgRemover
            )
            self.model.to(DEVICE)

        self.model.eval()

        image_tensor = self.preprocess(image_path)

        with torch.no_grad():
            output = self.model(image_tensor)

        mask_array = self.postprocess(output)

        return await self.remove_bg_by_segment(image_path, mask_array)


    @asyncHandler
    async def RemoveBackground(self, image_path):

        return await self._remove_background(image_path)