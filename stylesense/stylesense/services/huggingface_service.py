import requests
import os
from dotenv import load_dotenv
import base64

load_dotenv()

HF_TOKEN = os.getenv("HF_API_TOKEN", "")
HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def classify_fashion_image(image_bytes: bytes) -> dict:
    """Use HuggingFace fashion classification model"""
    API_URL = "https://api-inference.huggingface.co/models/nickmuchi/vit-finetuned-fashion"
    
    response = requests.post(
        API_URL,
        headers=HF_HEADERS,
        data=image_bytes
    )
    
    if response.status_code == 200:
        results = response.json()
        return {"classifications": results, "status": "success"}
    else:
        return {"classifications": [], "status": "error", "message": response.text}

def get_color_palette(image_bytes: bytes) -> dict:
    """Extract dominant colors using HuggingFace"""
    API_URL = "https://api-inference.huggingface.co/models/microsoft/resnet-50"
    
    response = requests.post(
        API_URL,
        headers=HF_HEADERS,
        data=image_bytes
    )
    
    if response.status_code == 200:
        return {"result": response.json(), "status": "success"}
    else:
        return {"result": [], "status": "error"}

def generate_fashion_text(prompt: str) -> str:
    """Use HuggingFace text generation for fashion descriptions"""
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    
    payload = {
        "inputs": f"[INST] You are a fashion expert. {prompt} [/INST]",
        "parameters": {"max_new_tokens": 300, "temperature": 0.7}
    }
    
    response = requests.post(API_URL, headers=HF_HEADERS, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "").split("[/INST]")[-1].strip()
    return "Unable to generate text at this time."

def semantic_fashion_search(query: str, items: list) -> list:
    """Use sentence transformers for semantic fashion search"""
    API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
    
    payload = {
        "inputs": {
            "source_sentence": query,
            "sentences": items
        }
    }
    
    response = requests.post(API_URL, headers=HF_HEADERS, json=payload)
    
    if response.status_code == 200:
        scores = response.json()
        ranked = sorted(zip(items, scores), key=lambda x: x[1], reverse=True)
        return [{"item": item, "score": score} for item, score in ranked]
    return []
