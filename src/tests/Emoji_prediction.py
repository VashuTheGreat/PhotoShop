import asyncio
import sys
import os
import hashlib
sys.path.append(os.getcwd())
from src.components.Generation_Emoji import Generation_Emoji

async def run_test():
    emoji_generator = Generation_Emoji()
    hashes = set()
    for i in range(5):
        buffer = await emoji_generator.GenerateEmoji()
        data = buffer.getvalue()
        md5 = hashlib.md5(data).hexdigest()
        print(f"Emoji {i} MD5: {md5}")
        hashes.add(md5)
    
    if len(hashes) == 1:
        print("ERROR: All generated emojis are identical!")
    else:
        print(f"SUCCESS: Generated {len(hashes)} unique emojis.")

if __name__ == "__main__":
    asyncio.run(run_test())