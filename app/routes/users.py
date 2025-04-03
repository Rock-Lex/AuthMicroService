from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User, AuthProviderEnum
from app.schemas import UserCreate, UserOut, UserOutCreated, UserUpdate, EmailUpdate, PasswordUpdate
from app.database import get_db
from app.utlis.security import create_email_confirmation_token, generate_hashed_password, generate_uuid, verify_password
from app.utlis.users_processing import get_user_by_email, process_user_creation, get_current_user
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

@router.get("", response_model=UserOut)
async def get_user(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.get("/confirm/{token}")
async def confirm_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.confirmation_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user.is_active = True
    user.confirmation_token = None
    db.commit()

    return {"type": "Success", "message": "Email confirmed successfully!"}


@router.put("/email", response_model=UserOut)
async def update_email(
        email_update: EmailUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    existing_user = db.query(User).filter(User.email == email_update.new_email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    current_user.email = email_update.new_email

    # Optionally require re-confirmation of the new email:
    # current_user.is_active = False
    # current_user.confirmation_token = create_email_confirmation_token(email_update.new_email)

    db.commit()
    db.refresh(current_user)

    # Optionally send a confirmation email:
    # send_confirmation_email.delay(current_user.email, current_user.confirmation_token)

    return current_user


@router.put("/password", response_model=dict)
async def update_password(
        password_update: PasswordUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Verify the current password matches the stored hash
    if not verify_password(password_update.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    current_user.hashed_password = generate_hashed_password(password_update.new_password)
    db.commit()

    return {"message": "Password updated successfully"}

@router.put("", response_model=UserOut)
async def update_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("", response_model=dict)
async def delete_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db.delete(current_user)
    db.commit()
    return {"message": "User deleted successfully"}
