from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

def chat_with_stylist(messages: list, system_prompt: str = None) -> str:
    if not system_prompt:
        system_prompt = """You are StyleSense AI, an expert fashion stylist with deep knowledge of:
- Current fashion trends and designer collections
- Personal styling for all body types and occasions
- Color theory and coordination
- Wardrobe building and capsule wardrobes
- Sustainable and budget-friendly fashion
- Cultural and seasonal fashion considerations

Provide personalized, actionable, and encouraging fashion advice. Be conversational, warm, and specific in your recommendations. Use emojis occasionally to keep things engaging."""

    chat_messages = [{"role": "system", "content": system_prompt}] + messages
    
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=chat_messages,
        max_tokens=1024,
        temperature=0.7
    )
    return response.choices[0].message.content

def get_quick_style_tip(context: str) -> str:
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are a concise fashion stylist. Give one powerful, actionable style tip in 2-3 sentences."
            },
            {"role": "user", "content": f"Give me a style tip about: {context}"}
        ],
        max_tokens=150,
        temperature=0.8
    )
    return response.choices[0].message.content

def generate_outfit_description(outfit_items: list) -> str:
    items_str = ", ".join(outfit_items)
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are a fashion copywriter. Write engaging, vivid outfit descriptions."
            },
            {
                "role": "user",
                "content": f"Write a stylish description for this outfit combination: {items_str}. Include the vibe, occasion suitability, and why it works. Keep it under 100 words."
            }
        ],
        max_tokens=200,
        temperature=0.9
    )
    return response.choices[0].message.content
