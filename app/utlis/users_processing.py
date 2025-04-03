from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models import User, AuthProviderEnum
from app.utlis.security import generate_uuid, generate_hashed_password, create_email_confirmation_token
from app.database import get_db
from app.utlis.security import verify_token


async def get_user_by_email(db, user_email):
    return db.query(User).filter(User.email == user_email).first()

def get_current_user(
    payload: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> User:
    user_uuid = payload.get("uuid")
    if not user_uuid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload."
        )
    user = db.query(User).filter(User.uuid == user_uuid).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found."
        )
    return user


def process_user_creation(db, user):
    user_uuid = generate_uuid()

    if user.password:
        hashed_password = generate_hashed_password(user.password)
        db_user = User(
            uuid=user_uuid,
            email=user.email,
            hashed_password=hashed_password,
            first_name=user.first_name,
            last_name=user.last_name,
            auth_provider=AuthProviderEnum.EMAIL,
            is_active=False
        )
    elif user.third_party_id:
        if user.auth_provider == "google":
            db_user = User(
                uuid=user_uuid,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                auth_provider=AuthProviderEnum.GOOGLE,
                third_party_id=user.third_party_id,
                is_active=True
            )
        elif user.auth_provider == "apple":
            db_user = User(
                uuid=user_uuid,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                auth_provider=AuthProviderEnum.APPLE,
                third_party_id=user.third_party_id,
                is_active=True
            )
        else:
            raise HTTPException(status_code=400, detail="Unsupported third-party provider")
    else:
        raise HTTPException(status_code=400, detail="Password or third-party ID must be provided")

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    confirmation_token = create_email_confirmation_token(user_uuid)

    db_user.confirmation_token = confirmation_token
    db.commit()

    return db_user, confirmation_token
