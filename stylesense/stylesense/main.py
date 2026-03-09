from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from routers import recommendations, analysis, trends, chat

app = FastAPI(
    title="StyleSense AI",
    description="Generative AI-Powered Fashion Recommendation System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Image Analysis"])
app.include_router(trends.router, prefix="/api/trends", tags=["Trends"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/recommendations")
async def recommendations_page(request: Request):
    return templates.TemplateResponse("recommendations.html", {"request": request})

@app.get("/analysis")
async def analysis_page(request: Request):
    return templates.TemplateResponse("analysis.html", {"request": request})

@app.get("/trends")
async def trends_page(request: Request):
    return templates.TemplateResponse("trends.html", {"request": request})

@app.get("/chat")
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
