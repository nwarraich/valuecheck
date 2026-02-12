from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.analyzer import analyze_listing
from routes.auth_routes import auth_router
from routes.analysis_routes import analysis_router

app = FastAPI()

# Allow frontend (HTML) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(analysis_router, prefix="/analyze", tags=["analyze"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
