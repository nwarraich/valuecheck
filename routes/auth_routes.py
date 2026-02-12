from fastapi import APIRouter
from pydantic import BaseModel

auth_router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    message: str

@auth_router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest):
    # Placeholder authentication
    return {
        "token": "placeholder-token",
        "message": f"Welcome, {data.username}"
    }

@auth_router.post("/logout")
def logout():
    return {"message": "Logged out"}
