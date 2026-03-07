from src.utils.asyncHandler import asyncHandler
from src.entity.S3_connect import S3
from src.constants import BUCKET_NAME, EMOJI_GENERATOR_MODEL_NAME, DEVICE
from src.utils.loader_functions import EmojiFaceGenerator

import torch
import matplotlib.pyplot as plt
import logging
import io
from PIL import Image

class Generation_Emoji:

    def __init__(self):
        self.s3 = S3(bucket_name=BUCKET_NAME)
        self.model = None

    @asyncHandler
    async def _generate_image(self, n_images=1):
        if self.model is None:
            self.model = await self.s3.loader(
                s3_key=EMOJI_GENERATOR_MODEL_NAME,
                loader_fn=EmojiFaceGenerator
            )

        self.model.eval()

        with torch.no_grad():

            z = torch.randn(n_images, 100).to(DEVICE)
            logging.info(f"Noise mean: {z.mean().item()}")
            images = self.model(z)
            # images = (images + 1) / 2
            images = torch.clamp(images, 0, 1)
            images = images.detach().cpu()

            img = images[0].numpy().transpose(1,2,0)

            img = (img * 255).astype("uint8")

            pil_image = Image.fromarray(img)

            buffer = io.BytesIO()
            pil_image.save(buffer, format="PNG")

            buffer.seek(0)

            return buffer


    @asyncHandler
    async def GenerateEmoji(self):
        return await self._generate_image()