from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from utils.gemini_client import get_gemini_recommendation
from utils.groq_client import get_groq_recommendation

router = APIRouter()

class UserPreferences(BaseModel):
    gender: str
    age_group: str
    style_preferences: List[str]
    occasion: str
    season: str
    color_preferences: Optional[List[str]] = []
    budget: Optional[str] = "medium"
    body_type: Optional[str] = ""
    ai_provider: Optional[str] = "gemini"

class RecommendationResponse(BaseModel):
    outfits: List[dict]
    styling_tips: List[str]
    trend_insights: str
    color_palette: List[str]

@router.post("/outfit", response_model=dict)
async def get_outfit_recommendation(preferences: UserPreferences):
    try:
        if preferences.ai_provider == "groq":
            result = await get_groq_recommendation(preferences.dict())
        else:
            result = await get_gemini_recommendation(preferences.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/capsule-wardrobe", response_model=dict)
async def get_capsule_wardrobe(preferences: UserPreferences):
    try:
        preferences_dict = preferences.dict()
        preferences_dict["request_type"] = "capsule_wardrobe"
        result = await get_gemini_recommendation(preferences_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/style-personas")
async def get_style_personas():
    personas = [
        {"id": "minimalist", "name": "Minimalist", "icon": "🤍", "description": "Clean lines, neutral tones, timeless pieces"},
        {"id": "bohemian", "name": "Bohemian", "icon": "🌸", "description": "Free-spirited, flowy fabrics, earthy tones"},
        {"id": "streetwear", "name": "Streetwear", "icon": "🔥", "description": "Urban, bold graphics, sneaker culture"},
        {"id": "classic", "name": "Classic Elegance", "icon": "👗", "description": "Sophisticated, tailored, timeless"},
        {"id": "athleisure", "name": "Athleisure", "icon": "💪", "description": "Sporty, comfortable, functional fashion"},
        {"id": "vintage", "name": "Vintage", "icon": "✨", "description": "Retro-inspired, nostalgic, unique finds"},
        {"id": "avant_garde", "name": "Avant-Garde", "icon": "🎨", "description": "Experimental, artistic, boundary-pushing"},
        {"id": "business", "name": "Business Chic", "icon": "💼", "description": "Professional, polished, power dressing"},
    ]
    return {"personas": personas}
