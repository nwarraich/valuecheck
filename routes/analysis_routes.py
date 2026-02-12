from fastapi import APIRouter
from pydantic import BaseModel
from backend.analyzer import analyze_listing

analysis_router = APIRouter()

class ListingRequest(BaseModel):
    listing_text: str

class AnalysisResponse(BaseModel):
    verdict: str
    estimated_range: str
    listed_price: str
    explanation: str

@analysis_router.post("", response_model=AnalysisResponse)
@analysis_router.post("/", response_model=AnalysisResponse)
def analyze(data: ListingRequest):
    result = analyze_listing(data.listing_text)
    return result
