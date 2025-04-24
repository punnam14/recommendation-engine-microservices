from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from .llm_service import LLMService

app = FastAPI(title="Recommendation Service")

llm_service = LLMService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserPreferences(BaseModel):
    priceRange: str = "all"
    categories: List[str] = []
    brands: List[str] = []

class RecommendationRequest(BaseModel):
    preferences: UserPreferences
    browsing_history: List[str] = []
    all_products: List[dict] = []

@app.post("/recommendations")
async def get_recommendations(req: RecommendationRequest):
    try:
        return llm_service.generate_recommendations(
            req.preferences.dict(),
            req.browsing_history,
            req.all_products
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
