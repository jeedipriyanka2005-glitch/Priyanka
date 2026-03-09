from fastapi import APIRouter, HTTPException
from models.schemas import UserPreferences, OutfitDescriptionRequest, StyleTipRequest
from services.gemini_service import get_fashion_recommendations
from services.groq_service import get_quick_style_tip, generate_outfit_description

router = APIRouter()

@router.post("/personalized")
async def get_personalized_recommendations(preferences: UserPreferences):
    try:
        prefs_dict = preferences.model_dump()
        recommendations = get_fashion_recommendations(prefs_dict)
        return {
            "status": "success",
            "recommendations": recommendations,
            "preferences": prefs_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/outfit-description")
async def describe_outfit(request: OutfitDescriptionRequest):
    try:
        description = generate_outfit_description(request.items)
        return {"status": "success", "description": description}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/style-tip")
async def get_style_tip(request: StyleTipRequest):
    try:
        tip = get_quick_style_tip(request.context)
        return {"status": "success", "tip": tip}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/occasions")
async def get_occasions():
    return {
        "occasions": [
            "Everyday Casual", "Work/Office", "Formal/Black Tie",
            "Date Night", "Wedding Guest", "Beach/Vacation",
            "Gym/Activewear", "Festival/Concert", "Business Casual",
            "Cocktail Party", "Brunch", "Night Out"
        ]
    }

@router.get("/styles")
async def get_styles():
    return {
        "styles": [
            "Minimalist", "Bohemian", "Streetwear", "Classic/Preppy",
            "Romantic", "Edgy/Rock", "Athleisure", "Business Professional",
            "Vintage/Retro", "Maximalist", "Scandinavian", "Y2K"
        ]
    }
