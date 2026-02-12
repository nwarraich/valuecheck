from fastapi import FastAPI
from pydantic import BaseModel
from analyser import analyze_listing
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend (HTML) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ListingRequest(BaseModel):
    listing_text: str

class AnalysisResponse(BaseModel):
    verdict: str
    estimated_range: str
    listed_price: str
    explanation: str

@app.post("/analyze", response_model=AnalysisResponse)
def analyze(data: ListingRequest):
    result = analyze_listing(data.listing_text)
    return result
