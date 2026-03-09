import google.generativeai as genai
import os
from dotenv import load_dotenv
import base64
from PIL import Image
import io

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))

def get_fashion_recommendations(preferences: dict) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""You are a professional fashion stylist AI. Based on the following user preferences, provide 5 detailed outfit recommendations.

User Preferences:
- Style: {preferences.get('style', 'casual')}
- Occasion: {preferences.get('occasion', 'everyday')}
- Season: {preferences.get('season', 'all-season')}
- Color Palette: {preferences.get('colors', 'neutral tones')}
- Budget: {preferences.get('budget', 'moderate')}
- Body Type: {preferences.get('body_type', 'not specified')}
- Gender: {preferences.get('gender', 'unisex')}

For each outfit provide:
1. Outfit name
2. Key pieces (top, bottom, footwear, accessories)
3. Color combinations
4. Why it works for this style/occasion
5. Styling tips

Format your response as structured outfit cards."""
    
    response = model.generate_content(prompt)
    return response.text

def analyze_fashion_image(image_bytes: bytes, analysis_type: str = "full") -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    image_data = base64.b64encode(image_bytes).decode("utf-8")
    
    prompts = {
        "full": """Analyze this fashion image comprehensively:
1. **Outfit Breakdown**: Identify all clothing items, colors, patterns
2. **Style Category**: (e.g., casual, formal, bohemian, streetwear, etc.)
3. **Color Palette**: Describe the color scheme and combinations
4. **Fit & Silhouette**: Analyze the overall look and proportions
5. **Occasion Suitability**: Where this outfit would work best
6. **Trend Analysis**: Current fashion trends reflected
7. **Styling Suggestions**: 3 ways to elevate or modify this outfit
8. **Similar Styles**: Recommend similar aesthetic directions""",
        "color": "Analyze the color palette in this fashion image. Identify all colors, suggest complementary colors, and provide color coordination tips.",
        "occasion": "Based on this outfit image, identify what occasions it's suitable for and suggest 3 alternative outfits for different occasions."
    }
    
    prompt = prompts.get(analysis_type, prompts["full"])
    
    response = model.generate_content([
        {"mime_type": "image/jpeg", "data": image_data},
        prompt
    ])
    return response.text

def get_trend_insights(category: str, season: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""As a fashion trend expert, provide detailed insights about current {season} {category} fashion trends.

Include:
1. **Top 5 Trending Styles** with descriptions
2. **Key Colors of the Season**
3. **Must-Have Pieces**
4. **Trending Patterns & Textures**
5. **Celebrity & Runway Influences**
6. **How to Style These Trends**
7. **Budget-Friendly Alternatives**
8. **Sustainability Angle**

Make it engaging, practical, and current."""
    
    response = model.generate_content(prompt)
    return response.text
