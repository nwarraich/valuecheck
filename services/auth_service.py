from backend.db import SessionLocal, User
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from utils.jwt_utils import create_token
from datetime import timedelta


def register_user(email: str, password: str):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            return {"error": "Email already taken"}, 400

        pw_hash = generate_password_hash(password)
        user = User(email=email, password=pw_hash)
        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_token({"sub": user.email}, expires_delta=timedelta(days=1))
        return {"token": token, "message": "Account created"}, 201
    except IntegrityError:
        db.rollback()
        return {"error": "Email already taken"}, 400
    except Exception as e:
        db.rollback()
        return {"error": str(e)}, 500
    finally:
        db.close()


def login_user(email: str, password: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user or not check_password_hash(user.password, password):
            return {"error": "Invalid credentials"}, 401

        token = create_token({"sub": user.email}, expires_delta=timedelta(days=1))
        return {"token": token, "message": "Logged in"}, 200
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        db.close()
