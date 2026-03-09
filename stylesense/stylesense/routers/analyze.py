from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional
from utils.gemini_client import analyze_outfit_image
import base64

router = APIRouter()

@router.post("/outfit-image")
async def analyze_outfit(
    file: UploadFile = File(...),
    analysis_type: Optional[str] = Form("full")
):
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        image_data = await file.read()
        if len(image_data) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image too large. Max 10MB.")
        
        image_b64 = base64.b64encode(image_data).decode("utf-8")
        result = await analyze_outfit_image(image_b64, file.content_type, analysis_type)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/color-palette")
async def extract_color_palette(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        image_data = await file.read()
        image_b64 = base64.b64encode(image_data).decode("utf-8")
        result = await analyze_outfit_image(image_b64, file.content_type, "color_palette")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/style-score")
async def get_style_score(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        image_data = await file.read()
        image_b64 = base64.b64encode(image_data).decode("utf-8")
        result = await analyze_outfit_image(image_b64, file.content_type, "style_score")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
