import fastapi

from fastapi.responses import StreamingResponse



from src.logger import logging
from src.components.Generation_Emoji import Generation_Emoji
emoji_generator = Generation_Emoji()
router=fastapi.APIRouter()



@router.get("/generate-emoji")
async def generate_emoji():
    try:
        logging.info("Generating emoji...")
        img_buffer = await emoji_generator.GenerateEmoji()
        headers = {
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
        return StreamingResponse(img_buffer, media_type="image/png", headers=headers)
    except Exception as e:
        logging.error(f"Error generating emoji: {str(e)}")
        return {"error": str(e)}