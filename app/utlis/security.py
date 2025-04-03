import uuid
import jwt
import datetime
from fastapi import Header, HTTPException, status
from passlib.context import CryptContext
from app.config import (PRIVATE_KEY,
                        PUBLIC_KEY,
                        JWT_ALGORITHM,
                        ACCESS_TOKEN_EXPIRE_MINUTES,
                        REFRESH_TOKEN_EXPIRE_DAYS,
                        logger)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(user_email: str, user_uuid: str):
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
        "uuid": str(user_uuid),
        "exp": expire,
        "jti": str(uuid.uuid4()),  # Unique identifier for the token
    }
    return jwt.encode(data, PRIVATE_KEY, algorithm=JWT_ALGORITHM)


def create_refresh_token(user_email: str, user_uuid: str):
    expire = datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_data = {
        "uuid": str(user_uuid),
        "exp": expire,
        "jti": str(uuid.uuid4()),  # Unique identifier for the refresh token
        "sub": user_email  # Add the user email (or user ID) here as the subject
    }
    return jwt.encode(refresh_data, PRIVATE_KEY, algorithm=JWT_ALGORITHM)

def create_email_confirmation_token(user_uuid: str) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    payload = {
        "uuid": str(user_uuid),
        "sub": str(user_uuid),
        "exp": expire
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str):
    try:
        return jwt.decode(token, PUBLIC_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def generate_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def generate_uuid() -> str:
    return str(uuid.uuid4())

def verify_token(authorization: str = Header(None)):  # Accept None to avoid error when missing
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing. Please include a valid 'Authorization' header."
        )

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme. Please use 'Bearer' scheme."
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected 'Bearer <token>'."
        )

    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired."
        )
    except jwt.InvalidTokenError as e:
        logger.error("JWT verification error: %s", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token."
        )

    return payload
