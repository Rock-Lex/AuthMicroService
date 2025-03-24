from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User, AuthProviderEnum
from app.schemas import UserCreate, UserOut, UserOutCreated
from app.database import get_db
from app.utlis.security import create_email_confirmation_token, generate_hashed_password, generate_uuid
from app.utlis.users_processing import get_user_by_email, process_user_creation
from email_tasks.tasks import send_confirmation_email
from app.config import logger
import uuid


router = APIRouter()

@router.post("", response_model=UserOutCreated)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        logger.warning(existing_user)
        raise HTTPException(status_code=400, detail="Email already registered")

    try:
        db_user, confirmation_token = process_user_creation(db, user)
    except HTTPException as e:
        raise e

    logger.debug(confirmation_token)
    # send_confirmation_email.delay(user.email, confirmation_token)

    return db_user

@router.get("/{user_uuid}", response_model=UserOut)
async def get_user(user_uuid: uuid.UUID, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.uuid == user_uuid).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/confirm/{token}")
async def confirm_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.confirmation_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user.is_active = True
    user.confirmation_token = None
    db.commit()

    return {"type": "Success", "message": "Email confirmed successfully!"}