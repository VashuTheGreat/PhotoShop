import fastapi

from fastapi.responses import StreamingResponse
from fastapi import UploadFile,File
import os
import shutil
import tempfile



from src.logger import logging
from src.components.Removed_background import RemovedBackground
removed_background = RemovedBackground()
router=fastapi.APIRouter()



@router.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    temp_path = None
    try:
        logging.info(f"Removing background from uploaded file: {file.filename}")
        
        # Save uploaded file to a temporary location
        extension = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name
        
        # Process the image
        mask_buffer = await removed_background.RemoveBackground(temp_path)
        
        return StreamingResponse(mask_buffer, media_type="image/png")
    
    except Exception as e:
        logging.error(f"Error removing background: {str(e)}")
        return {"error": str(e)}
    
    finally:
        # Cleanup temporary file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)