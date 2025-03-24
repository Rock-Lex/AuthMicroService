import uuid
import jwt
import datetime
from passlib.context import CryptContext
from app.config import PRIVATE_KEY, PUBLIC_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(user_email: str):
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
        "exp": expire,
        "jti": str(uuid.uuid4()),  # Unique identifier for the token
    }
    return jwt.encode(data, PRIVATE_KEY, algorithm=JWT_ALGORITHM)


def create_refresh_token(user_email: str):
    expire = datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_data = {
        "exp": expire,
        "jti": str(uuid.uuid4()),  # Unique identifier for the refresh token
        "sub": user_email  # Add the user email (or user ID) here as the subject
    }
    return jwt.encode(refresh_data, PRIVATE_KEY, algorithm=JWT_ALGORITHM)

def create_email_confirmation_token(user_uuid: str) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    payload = {
        "sub": user_uuid,
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