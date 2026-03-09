from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, SearchRequest
from services.groq_service import chat_with_stylist
from services.huggingface_service import semantic_fashion_search

router = APIRouter()

@router.post("/message")
async def send_message(request: ChatRequest):
    try:
        messages = [{"role": m.role, "content": m.content} for m in request.messages]
        
        context_prompt = None
        if request.context:
            context_prompt = f"""You are StyleSense AI, an expert fashion stylist. 
Context: {request.context}
Provide personalized, actionable fashion advice. Be warm, specific, and encouraging."""
        
        response = chat_with_stylist(messages, context_prompt)
        return {"status": "success", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search")
async def semantic_search(request: SearchRequest):
    try:
        results = semantic_fashion_search(request.query, request.items)
        return {"status": "success", "results": results, "query": request.query}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
