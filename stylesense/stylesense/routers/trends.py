from fastapi import APIRouter, HTTPException
from models.schemas import TrendRequest
from services.gemini_service import get_trend_insights

router = APIRouter()

@router.post("/insights")
async def get_trends(request: TrendRequest):
    try:
        insights = get_trend_insights(request.category, request.season)
        return {
            "status": "success",
            "category": request.category,
            "season": request.season,
            "insights": insights
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_trend_categories():
    return {
        "categories": [
            {"id": "women", "label": "Women's Fashion", "icon": "👗"},
            {"id": "men", "label": "Men's Fashion", "icon": "👔"},
            {"id": "streetwear", "label": "Streetwear", "icon": "🧢"},
            {"id": "accessories", "label": "Accessories", "icon": "👜"},
            {"id": "footwear", "label": "Footwear", "icon": "👟"},
            {"id": "sustainable", "label": "Sustainable Fashion", "icon": "🌿"},
            {"id": "luxury", "label": "Luxury Fashion", "icon": "💎"},
            {"id": "activewear", "label": "Activewear", "icon": "🏃"},
        ],
        "seasons": ["Spring/Summer 2025", "Fall/Winter 2025", "Resort 2025", "Current Season"]
    }
