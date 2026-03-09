from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from services.gemini_service import analyze_fashion_image
from services.huggingface_service import classify_fashion_image

router = APIRouter()

@router.post("/image")
async def analyze_image(
    file: UploadFile = File(...),
    analysis_type: str = Form(default="full")
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")
    
    try:
        image_bytes = await file.read()
        
        # Gemini deep analysis
        gemini_analysis = analyze_fashion_image(image_bytes, analysis_type)
        
        # HuggingFace classification (parallel)
        hf_classification = classify_fashion_image(image_bytes)
        
        return {
            "status": "success",
            "filename": file.filename,
            "analysis_type": analysis_type,
            "gemini_analysis": gemini_analysis,
            "hf_classification": hf_classification
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/color-analysis")
async def analyze_colors(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")
    
    try:
        image_bytes = await file.read()
        analysis = analyze_fashion_image(image_bytes, "color")
        return {"status": "success", "color_analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/occasion-match")
async def match_occasion(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")
    
    try:
        image_bytes = await file.read()
        analysis = analyze_fashion_image(image_bytes, "occasion")
        return {"status": "success", "occasion_analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
