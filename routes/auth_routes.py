from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.auth_service import register_user, login_user

auth_router = APIRouter()


class RegisterRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    token: str = None
    message: str


@auth_router.post("/register", response_model=AuthResponse)
def register(data: RegisterRequest):
    body, status = register_user(data.email, data.password)
    if status >= 400:
        raise HTTPException(status_code=status, detail=body.get("error", "Registration failed"))
    return body


class LoginRequest(BaseModel):
    email: str
    password: str


@auth_router.post("/login", response_model=AuthResponse)
def login(data: LoginRequest):
    body, status = login_user(data.email, data.password)
    if status >= 400:
        raise HTTPException(status_code=status, detail=body.get("error", "Invalid credentials"))
    return body


@auth_router.post("/logout")
def logout():
    return {"message": "Logged out"}
