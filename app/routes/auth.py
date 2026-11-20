import jwt
from fastapi import APIRouter, HTTPException
from passlib.hash import pbkdf2_sha256 as password_hash 
from datetime import datetime, timedelta, timezone
router = APIRouter(prefix="/auth")
from app.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.schemas import user


def create_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload

    except jwt.InvalidTokenError:
        return None


@router.post("/login")
def login(user: UserLogin):

    # Find user in your users list
    existing_user = None

    for u in users:
        if u["username"] == user.username:
            existing_user = u
            break

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not password_hash.verify(user.password, existing_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(existing_user["id"])

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/register")
def register(user: UserCreate):

    hashed_password = password_hash.hash(user.password)

    new_user = {
        "id": len(users) + 1,
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password
    }

    users.append(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user["id"]
    }