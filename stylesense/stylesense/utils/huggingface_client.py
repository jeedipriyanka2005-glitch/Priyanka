import httpx
from config import HUGGINGFACE_API_TOKEN

HF_API_URL = "https://api-inference.huggingface.co/models"

async def classify_fashion_item(image_b64: str) -> dict:
    """Use HuggingFace model to classify fashion items."""
    try:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
        
        import base64
        image_bytes = base64.b64decode(image_b64)
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{HF_API_URL}/google/vit-base-patch16-224",
                headers=headers,
                content=image_bytes
            )
            
            if response.status_code == 200:
                results = response.json()
                return {
                    "classifications": results[:5] if isinstance(results, list) else results,
                    "provider": "Hugging Face (ViT)"
                }
            else:
                return {"error": f"HF API error: {response.status_code}", "provider": "Hugging Face"}
                
    except Exception as e:
        return {"error": str(e), "provider": "Hugging Face"}


async def get_fashion_embeddings(text: str) -> dict:
    """Get text embeddings for fashion similarity search."""
    try:
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{HF_API_URL}/sentence-transformers/all-MiniLM-L6-v2",
                headers=headers,
                json={"inputs": text}
            )
            
            if response.status_code == 200:
                return {"embeddings": response.json(), "provider": "Hugging Face"}
            else:
                return {"error": f"HF API error: {response.status_code}"}
                
    except Exception as e:
        return {"error": str(e)}


async def generate_fashion_image_caption(image_b64: str) -> dict:
    """Generate caption for fashion image."""
    try:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
        
        import base64
        image_bytes = base64.b64decode(image_b64)
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{HF_API_URL}/Salesforce/blip-image-captioning-base",
                headers=headers,
                content=image_bytes
            )
            
            if response.status_code == 200:
                result = response.json()
                caption = result[0].get("generated_text", "") if isinstance(result, list) else str(result)
                return {"caption": caption, "provider": "Hugging Face (BLIP)"}
            else:
                return {"error": f"HF API error: {response.status_code}"}
                
    except Exception as e:
        return {"error": str(e)}
