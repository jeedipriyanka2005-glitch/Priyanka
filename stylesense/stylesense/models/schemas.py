from pydantic import BaseModel
from typing import Optional, List

class UserPreferences(BaseModel):
    style: Optional[str] = "casual"
    occasion: Optional[str] = "everyday"
    season: Optional[str] = "all-season"
    colors: Optional[str] = "neutral tones"
    budget: Optional[str] = "moderate"
    body_type: Optional[str] = "not specified"
    gender: Optional[str] = "unisex"
    age_group: Optional[str] = "adult"

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    context: Optional[str] = None

class TrendRequest(BaseModel):
    category: str = "general"
    season: str = "current"
    gender: Optional[str] = "unisex"

class OutfitDescriptionRequest(BaseModel):
    items: List[str]

class StyleTipRequest(BaseModel):
    context: str

class SearchRequest(BaseModel):
    query: str
    items: List[str]
