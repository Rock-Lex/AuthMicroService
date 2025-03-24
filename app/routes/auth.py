from fastapi import APIRouter, Depends, HTTPException
from app.utlis.security import decode_access_token, create_access_token, create_refresh_token
from app.utlis.auth_processing import login
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import AuthToken, LoginForm, RefreshTokenRequest

router = APIRouter()

@router.post("/login", response_model=AuthToken)
async def login_user(login_data: LoginForm, db: Session = Depends(get_db)):
    return await login(login_data, db)

@router.post("/refresh", response_model=AuthToken)
async def refresh_token(refresh_token_request: RefreshTokenRequest):
    refresh_token = refresh_token_request.refresh_token
    payload = decode_access_token(refresh_token)

    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user_email = payload["sub"]

    new_access_token = create_access_token(user_email=user_email)

    return {"type": "Success", "access_token": new_access_token, "refresh_token": refresh_token, "token_type": "bearer"}