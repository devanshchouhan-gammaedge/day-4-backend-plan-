from fastapi import APIRouter, HTTPException , Depends
import jwt
from datetime import datetime, timedelta, timezone
from app.schemas.user_model import UserSignup, UserResponse , UserLogin
from app.data import users, next_user_id
from passlib.hash import pbkdf2_sha256 as password_hash
from app import data 
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials 


bearer_scheme = HTTPBearer()
router =APIRouter(prefix="/auth")
SECRET_KEY = "my-super-secret-key-change-later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    token = credentials.credentials
    payload = verify_token(token)
    return payload
def create_access_token(user_id: int , role: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, 
                            detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, 
                            detail="Invalid token")
    
@router.post("/signup", response_model=UserResponse)
def signup(user: UserSignup):
    global next_user_id

    for existing_user in users:
        if existing_user["username"] == user.username:
            raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = password_hash.hash(user.password)

    new_user = {
        "id": next_user_id,
        "username": user.username,
        "password": hashed_password,
        "role": "user"
    }

    users.append(new_user)
    next_user_id += 1   

    return new_user



@router.post("/login")
def login(user: UserLogin):
    for existing_user in users:
        if existing_user["username"] == user.username:
            if password_hash.verify(user.password, existing_user["password"]):
                  token = create_access_token(
                    user_id=existing_user["id"],
                    role=existing_user["role"]
                     )
                #   decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                #   print(f"Decoded token: {decoded_token}")
                  decoded_token = verify_token(token)

                  print("Verified payload:", decoded_token)
                  return {"message": "Login successful" , "user": existing_user, "access_token": token , "token_type": "bearer"}  
            else:
                raise HTTPException(status_code=401, detail="Invalid password")
    raise HTTPException(status_code=404, detail="User not found")


