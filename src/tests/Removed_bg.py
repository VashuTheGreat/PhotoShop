import asyncio
import sys
import os
sys.path.append(os.getcwd())
from src.logger import *
from src.components.Removed_background import RemovedBackground
removed_background=RemovedBackground()

async def main():
    img_buffer = await removed_background.RemoveBackground("public/test1.jpg")
    with open("public/result_bg_removed.png", "wb") as f:
        f.write(img_buffer.getvalue())
    print("Background removal completed. Result saved to public/result_bg_removed.png")

if __name__ == "__main__":
    asyncio.run(main())