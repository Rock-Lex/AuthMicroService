from fastapi import HTTPException
from app.models import User
from app.utlis.security import verify_password, create_access_token, create_refresh_token



"""
# Login
"""

async def login(form_data, db):
    # Extract the provider from the request (could be part of the request body or query params)
    provider = form_data.provider if hasattr(form_data, "provider") else "email"

    if provider == "email":
        return await email_login(form_data, db)
    elif provider == "google":
        return await google_login(form_data, db)
    elif provider == "apple":
        return await apple_login(form_data, db)
    else:
        raise HTTPException(status_code=400, detail="Unsupported authentication provider")


async def email_login(form_data, db):
    # Use form_data.email instead of form_data.username
    email = form_data.email
    password = form_data.password

    # Fetch user by email
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate access and refresh tokens
    access_token = create_access_token(user_email=user.email, user_uuid=user.uuid)
    refresh_token = create_refresh_token(user_email=user.email, user_uuid=user.uuid)

    # Return the tokens and token type
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


async def google_login(form_data, db):
    # Handle Google login logic here (e.g., verify the Google token)
    pass


async def apple_login(form_data, db):
    # Handle Apple login logic here (e.g., verify the Apple token)
    pass