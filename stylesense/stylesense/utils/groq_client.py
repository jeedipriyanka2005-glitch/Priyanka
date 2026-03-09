from groq import Groq
from config import GROQ_API_KEY
import json
import re

GROQ_SYSTEM_PROMPT = """You are StyleSense, an expert AI fashion stylist. You have expertise in:
- Current 2024-2025 fashion trends
- Color theory, coordination, and styling
- Body type styling and flattering silhouettes
- Occasion-appropriate dressing
- Budget-conscious and sustainable fashion choices
- Global fashion aesthetics and cultural styles

Provide specific, actionable, personalized advice. Return valid JSON when requested."""

def _extract_json(text: str) -> dict:
    try:
        return json.loads(text)
    except:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
        return {"raw_response": text}


async def get_groq_recommendation(preferences: dict) -> dict:
    """Get outfit recommendations from Groq (Llama)."""
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        prompt = f"""Generate 3 personalized outfit recommendations as JSON.

User: {preferences.get('gender')}, {preferences.get('age_group')}
Style: {', '.join(preferences.get('style_preferences', []))}
Occasion: {preferences.get('occasion')}
Season: {preferences.get('season')}
Colors: {', '.join(preferences.get('color_preferences', []))}
Budget: {preferences.get('budget')}

Return ONLY this JSON structure:
{{
  "outfits": [
    {{
      "name": "outfit name",
      "description": "description",
      "pieces": [{{"item": "item name", "color": "color", "style_note": "note"}}],
      "occasion_suitability": "suitable for",
      "confidence_score": 90,
      "budget_estimate": "$XX-$XX",
      "styling_tip": "tip"
    }}
  ],
  "color_palette": ["#hex1", "#hex2", "#hex3"],
  "styling_tips": ["tip1", "tip2"],
  "trend_insights": "insights",
  "accessories_guide": "guide"
}}"""
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": GROQ_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        result = _extract_json(completion.choices[0].message.content)
        result["provider"] = "Groq (Llama 3.3)"
        return result
        
    except Exception as e:
        return {
            "error": str(e),
            "outfits": [],
            "styling_tips": ["Please configure your Groq API key in .env file"],
            "provider": "Groq (Llama 3.3)"
        }


async def get_groq_trends(request: dict) -> dict:
    """Get fashion trends from Groq."""
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        prompt = f"""Provide fashion trend insights for {request.get('season')} {request.get('year')}.
Category: {request.get('category')}, Region: {request.get('region')}

Return ONLY valid JSON:
{{
  "headline_trends": [
    {{"trend_name": "name", "description": "desc", "key_pieces": ["piece"], "how_to_wear": "tip", "longevity": "macro trend", "accessibility": "mid-range"}}
  ],
  "color_trends": [{{"color_name": "name", "hex": "#XXXXXX", "description": "desc", "styling_tip": "tip"}}],
  "fabric_trends": ["fabric1"],
  "street_style_insights": "insights",
  "sustainability_highlights": "highlights",
  "shopping_guide": "guide"
}}"""
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": GROQ_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        result = _extract_json(completion.choices[0].message.content)
        result["provider"] = "Groq (Llama 3.3)"
        return result
        
    except Exception as e:
        return {"error": str(e), "provider": "Groq (Llama 3.3)"}


async def chat_with_groq_stylist(message: str, history: list, user_context: dict) -> dict:
    """Chat with Groq AI stylist."""
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        messages = [{"role": "system", "content": GROQ_SYSTEM_PROMPT}]
        
        for msg in history[-10:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        messages.append({"role": "user", "content": message})
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1000,
            temperature=0.8
        )
        
        return {
            "response": completion.choices[0].message.content,
            "provider": "Groq (Llama 3.3)"
        }
        
    except Exception as e:
        return {
            "response": f"Unable to connect to Groq. Please configure GROQ_API_KEY. Error: {str(e)}",
            "provider": "Groq (Llama 3.3)"
        }
