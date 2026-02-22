from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from backend.db import SessionLocal, User
import secrets

auth_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class RegisterRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    token: str
    message: str


@auth_router.post("/register", response_model=AuthResponse)
def register(data: RegisterRequest, db=Depends(get_db)):
    # Check if user exists
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    pw_hash = generate_password_hash(data.password)
    user = User(username=data.username, password_hash=pw_hash)
    db.add(user)
    db.commit()
    db.refresh(user)

    token = secrets.token_urlsafe(24)
    return {"token": token, "message": "Account created"}


class LoginRequest(BaseModel):
    username: str
    password: str


@auth_router.post("/login", response_model=AuthResponse)
def login(data: LoginRequest, db=Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not check_password_hash(user.password_hash, data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = secrets.token_urlsafe(24)
    return {"token": token, "message": f"Welcome, {user.username}"}


@auth_router.post("/logout")
def logout():
    return {"message": "Logged out"}
