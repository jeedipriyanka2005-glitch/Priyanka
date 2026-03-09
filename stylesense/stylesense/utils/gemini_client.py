import google.generativeai as genai
from config import GEMINI_API_KEY
import json
import re

genai.configure(api_key=GEMINI_API_KEY)

FASHION_SYSTEM_PROMPT = """You are StyleSense, an expert AI fashion stylist with deep knowledge of:
- Current fashion trends (2024-2025)
- Color theory and coordination
- Body type styling
- Occasion-appropriate dressing
- Sustainable and budget-conscious fashion
- Global fashion cultures and aesthetics

Always provide specific, actionable, and personalized advice. Format responses as valid JSON when requested."""

def _extract_json(text: str) -> dict:
    """Extract JSON from model response."""
    try:
        # Try direct parse
        return json.loads(text)
    except:
        # Try to find JSON block
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
        return {"raw_response": text}


async def get_gemini_recommendation(preferences: dict) -> dict:
    """Get outfit recommendations from Gemini."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        request_type = preferences.get("request_type", "outfit")
        
        if request_type == "capsule_wardrobe":
            prompt = f"""Create a complete capsule wardrobe recommendation.

User Profile:
- Gender: {preferences.get('gender')}
- Age Group: {preferences.get('age_group')}
- Style: {', '.join(preferences.get('style_preferences', []))}
- Season: {preferences.get('season')}
- Budget: {preferences.get('budget')}
- Body Type: {preferences.get('body_type', 'not specified')}

Return ONLY valid JSON:
{{
  "capsule_essentials": [
    {{"category": "string", "item": "string", "why_essential": "string", "versatility_score": 9, "suggested_colors": ["color1"]}}
  ],
  "outfit_combinations": [
    {{"name": "string", "pieces": ["piece1", "piece2"], "occasion": "string", "description": "string"}}
  ],
  "investment_pieces": ["item1", "item2"],
  "budget_breakdown": {{"total_estimate": "string", "priority_order": ["item1"]}},
  "styling_philosophy": "string",
  "seasonal_adaptations": "string"
}}"""
        else:
            prompt = f"""Generate personalized outfit recommendations.

User Profile:
- Gender: {preferences.get('gender')}
- Age Group: {preferences.get('age_group')}
- Style Preferences: {', '.join(preferences.get('style_preferences', []))}
- Occasion: {preferences.get('occasion')}
- Season: {preferences.get('season')}
- Color Preferences: {', '.join(preferences.get('color_preferences', []))}
- Budget: {preferences.get('budget')}
- Body Type: {preferences.get('body_type', 'not specified')}

Return ONLY valid JSON:
{{
  "outfits": [
    {{
      "name": "string",
      "description": "string",
      "pieces": [
        {{"item": "string", "color": "string", "style_note": "string"}}
      ],
      "occasion_suitability": "string",
      "confidence_score": 95,
      "budget_estimate": "string",
      "styling_tip": "string"
    }}
  ],
  "color_palette": ["hex1", "hex2", "hex3", "hex4"],
  "styling_tips": ["tip1", "tip2", "tip3"],
  "trend_insights": "string",
  "accessories_guide": "string",
  "care_tips": "string"
}}"""
        
        response = model.generate_content(
            [FASHION_SYSTEM_PROMPT + "\n\n" + prompt]
        )
        
        result = _extract_json(response.text)
        result["provider"] = "Google Gemini"
        return result
        
    except Exception as e:
        return {
            "error": str(e),
            "outfits": [],
            "styling_tips": ["Please configure your Gemini API key in .env file"],
            "trend_insights": "API key required",
            "color_palette": [],
            "provider": "Google Gemini"
        }


async def analyze_outfit_image(image_b64: str, content_type: str, analysis_type: str) -> dict:
    """Analyze outfit image using Gemini Vision."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompts = {
            "full": """Analyze this outfit comprehensively. Return ONLY valid JSON:
{
  "overall_style": "string",
  "style_category": "string",
  "identified_pieces": [{"item": "string", "color": "string", "pattern": "string", "estimated_brand_style": "string"}],
  "color_analysis": {"dominant_colors": ["color1"], "color_harmony": "string", "palette_type": "string"},
  "occasion_suitability": ["occasion1", "occasion2"],
  "style_score": 8,
  "strengths": ["strength1", "strength2"],
  "improvement_suggestions": ["suggestion1", "suggestion2"],
  "similar_styles": ["style1", "style2"],
  "trend_alignment": "string",
  "estimated_price_range": "string",
  "seasonal_appropriateness": "string",
  "accessory_recommendations": ["accessory1", "accessory2"]
}""",
            "color_palette": """Extract the color palette from this outfit. Return ONLY valid JSON:
{
  "colors": [{"name": "string", "hex": "#XXXXXX", "percentage": 30, "role": "dominant/accent/neutral"}],
  "palette_type": "string",
  "color_harmony": "string",
  "mood": "string",
  "complementary_colors": ["#hex1"],
  "seasonal_palette": "string"
}""",
            "style_score": """Score this outfit's style. Return ONLY valid JSON:
{
  "overall_score": 8,
  "breakdown": {
    "color_coordination": 8,
    "fit_appropriateness": 7,
    "trend_relevance": 9,
    "occasion_match": 8,
    "accessory_balance": 7
  },
  "verdict": "string",
  "celebrity_style_match": "string",
  "improvement_tips": ["tip1", "tip2"],
  "compliments": ["compliment1", "compliment2"]
}"""
        }
        
        prompt = prompts.get(analysis_type, prompts["full"])
        
        image_part = {
            "inline_data": {
                "mime_type": content_type,
                "data": image_b64
            }
        }
        
        response = model.generate_content([prompt, image_part])
        result = _extract_json(response.text)
        result["provider"] = "Google Gemini Vision"
        return result
        
    except Exception as e:
        return {"error": str(e), "provider": "Google Gemini Vision"}


async def get_trend_insights(request: dict) -> dict:
    """Get fashion trend insights from Gemini."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""Provide comprehensive fashion trend insights.

Parameters:
- Season: {request.get('season')}
- Year: {request.get('year', 2025)}
- Category: {request.get('category', 'all')}
- Region: {request.get('region', 'global')}

Return ONLY valid JSON:
{{
  "headline_trends": [
    {{
      "trend_name": "string",
      "description": "string",
      "key_pieces": ["piece1"],
      "how_to_wear": "string",
      "celebrity_advocates": ["name1"],
      "longevity": "micro/macro/mega trend",
      "accessibility": "luxury/mid-range/budget"
    }}
  ],
  "color_trends": [
    {{"color_name": "string", "hex": "#XXXXXX", "description": "string", "styling_tip": "string"}}
  ],
  "fabric_trends": ["fabric1", "fabric2"],
  "silhouette_trends": ["silhouette1"],
  "key_brands_to_watch": ["brand1", "brand2"],
  "street_style_insights": "string",
  "sustainability_highlights": "string",
  "shopping_guide": "string",
  "trend_forecast": "string"
}}"""
        
        response = model.generate_content([FASHION_SYSTEM_PROMPT + "\n\n" + prompt])
        result = _extract_json(response.text)
        result["provider"] = "Google Gemini"
        return result
        
    except Exception as e:
        return {"error": str(e), "provider": "Google Gemini"}


async def chat_with_stylist(message: str, history: list, user_context: dict) -> dict:
    """Chat with AI stylist using Gemini."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        context = ""
        if user_context:
            context = f"\nUser Context: {json.dumps(user_context)}\n"
        
        conversation = FASHION_SYSTEM_PROMPT + context + "\n\nConversation History:\n"
        for msg in history[-10:]:  # Last 10 messages
            role = "User" if msg["role"] == "user" else "StyleSense"
            conversation += f"{role}: {msg['content']}\n"
        
        conversation += f"\nUser: {message}\nStyleSense:"
        
        response = model.generate_content([conversation])
        
        return {
            "response": response.text,
            "provider": "Google Gemini",
            "suggestions": []
        }
        
    except Exception as e:
        return {
            "response": f"I'm having trouble connecting right now. Please ensure your Gemini API key is configured. Error: {str(e)}",
            "provider": "Google Gemini",
            "suggestions": []
        }
