# StyleSense AI 👗✨
### Generative AI-Powered Fashion Recommendation System

## Overview
StyleSense AI is a full-stack fashion recommendation platform powered by multiple AI models including Google Gemini, Groq (LLaMA), and HuggingFace.

## Features
- 🎯 **Personalized Recommendations** – AI outfit suggestions based on style, occasion, budget, season
- 📸 **Style Analysis** – Upload outfit photos for deep visual analysis
- 🔥 **Trend Intelligence** – Season-aware fashion trend insights
- 💬 **AI Stylist Chat** – Real-time conversational stylist powered by Groq

## Tech Stack
- **Backend:** FastAPI, Python 3.10+
- **AI Models:** Google Gemini 1.5 Flash, Groq LLaMA 3 70B, HuggingFace Transformers
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Templating:** Jinja2

## Setup Instructions

### 1. Clone / Download the project
```bash
cd stylesense
```

### 2. Create virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
```bash
cp .env.example .env
```
Edit `.env` and add your API keys:
- **GEMINI_API_KEY** → https://aistudio.google.com/app/apikey
- **GROQ_API_KEY** → https://console.groq.com/
- **HF_API_TOKEN** → https://huggingface.co/settings/tokens

### 5. Run the application
```bash
uvicorn main:app --reload
```

### 6. Open in browser
```
http://localhost:8000
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/recommendations/personalized` | Get outfit recommendations |
| POST | `/api/analysis/image` | Analyze outfit photo |
| POST | `/api/trends/insights` | Get trend insights |
| POST | `/api/chat/message` | Chat with AI stylist |

## Project Structure
```
stylesense/
├── main.py              # FastAPI app entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── routers/             # API route handlers
│   ├── recommendations.py
│   ├── analysis.py
│   ├── trends.py
│   └── chat.py
├── services/            # AI service integrations
│   ├── gemini_service.py
│   ├── groq_service.py
│   └── huggingface_service.py
├── models/              # Pydantic schemas
│   └── schemas.py
├── templates/           # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── recommendations.html
│   ├── analysis.html
│   ├── trends.html
│   └── chat.html
└── static/              # Frontend assets
    ├── css/style.css
    └── js/
        ├── main.js
        ├── recommendations.js
        ├── analysis.js
        ├── trends.js
        └── chat.js
```
