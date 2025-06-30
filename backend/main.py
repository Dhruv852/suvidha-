from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime
from utils.knowledge_base import KnowledgeBase
import logging
from fastapi.staticfiles import StaticFiles

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="GFR & PM Assistant API",
    description="API for intelligent GFR and PM document processing and querying",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://suvidha-iota.vercel.app"  # Replace with your actual Vercel domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add static file serving
app.mount("/static", StaticFiles(directory="data"), name="static")

# Initialize Gemini API with specific model and key
GEMINI_API_KEY = "AIzaSyA7zvS_Z97Eeb1Ue5M0ZNn-H8UFIKBcY4M"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Initialize knowledge base
knowledge_base = KnowledgeBase(
    data_dir="data",
    vector_store_dir="vector_store"
)

# Pydantic models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[Message]

class Citation(BaseModel):
    rule_number: str
    text: str
    source: str
    page: int

class ChatResponse(BaseModel):
    response: str
    citations: List[Citation]

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Format conversation history for Gemini
        chat = model.start_chat(history=[
            {"role": msg.role, "parts": [msg.content]} 
            for msg in request.history
        ])
        
        # Get response from Gemini
        response = chat.send_message(request.message)
        
        # Search knowledge base for relevant rules from both GFR and PM
        gfr_results = []
        pm_results = []
        
        # Get all search results
        all_results = knowledge_base.search(request.message, k=6)  # Increased k to get more results
        
        # Separate results by source
        for result in all_results:
            rule = result["rule"]
            if rule.source == "GFR 2017":
                gfr_results.append(result)
            elif rule.source == "PM 2025":
                pm_results.append(result)
        
        # Take top 2 results from each source if available
        citations = []
        for result in gfr_results[:2]:
            rule = result["rule"]
            citations.append(Citation(
                rule_number=rule.rule_number,
                text=rule.text,
                source=rule.source,
                page=rule.page
            ))
        
        for result in pm_results[:2]:
            rule = result["rule"]
            citations.append(Citation(
                rule_number=rule.rule_number,
                text=rule.text,
                source=rule.source,
                page=rule.page
            ))
        
        return ChatResponse(
            response=response.text,
            citations=citations
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Document processing endpoint
@app.post("/process-documents")
async def process_documents():
    try:
        # TODO: Implement document processing
        return {"status": "processing", "message": "Document processing started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 