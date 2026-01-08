from fastapi import APIRouter, HTTPException, Response
from bcrypt import hashpw, gensalt, checkpw
from pydantic import BaseModel
from jose import jwt, JWTError # type: ignore  # (there are no stubs available)
from os import getenv
from datetime import datetime, timedelta, timezone

from ..database import database, database_models

router = APIRouter()

ALGORITHM = "HS256"
SECRET_KEY = getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Add a JWT secret key to environment")

def generate_jwt_token(account_id: int) -> str:
    now = datetime.now(timezone.utc)
    jwt_payload = {
        "sub": str(account_id),
        "exp": now + timedelta(days=7),
        "iat": now
    }
    return jwt.encode(jwt_payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        return None

class RegisterRequest(BaseModel):
    email: str
    password: str

@router.post("/register", status_code=201)
async def register(req: RegisterRequest):
    # check if email in use
    exists = await database.fetchone(
        "SELECT * FROM accounts WHERE email = %s",
        (req.email,),
        database_models.Account
    )
    if exists:
        raise HTTPException(409, "This email is associated to an existing account.")

    # salt and hash password and store it
    hashed = hashpw(req.password.encode("utf-8"), gensalt()).decode()
    await database.execute(
        "INSERT INTO accounts (email, password_hash) VALUES (%s, %s)",
        (req.email, hashed,),
    )

    return {"status": "ok", "msg": "Account successfully created"}
    

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(req: LoginRequest, response: Response):
    # find user and verify correct password
    user = await database.fetchone(
        "SELECT * FROM accounts WHERE email = %s",
        (req.email,),
        database_models.Account
    )
    if not user or not checkpw(req.password.encode("utf-8"), user.password_hash.encode("utf-8")):
        raise HTTPException(status_code=403, detail="Invalid login")

    # create jwt token
    jwt_token = generate_jwt_token(user.account_id)

    response.set_cookie(
        "jwt_token",
        jwt_token,
        httponly=True,
        samesite="lax",
        secure=True,
        max_age=int(timedelta(days=7).total_seconds())
    )

    return {"status": "ok", "msg": "Sucessful login"}
