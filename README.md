# **Authentication Microservice on FastAPI** 🔐  

An **asynchronous, high-performance authentication microservice** built with **FastAPI** and **PostgreSQL**, designed to handle secure user authentication, JWT token-based authorization, email confirmation, and third-party authentication providers.  

## **🚀 Features**  
- **User Authentication & Registration** 🔑  
  - Secure user registration with email and hashed password  
  - Authentication using **JWT (RS256 asymmetric encryption)**  
  - Third-party authentication support (Google, Apple, etc.)  
  
- **Token-Based Security** 🔐  
  - **Access & Refresh tokens** for session management  
  - **Public-private key verification** to authenticate tokens across services  
  - Secure **refresh token mechanism** (without storing tokens in a database)  
  
- **Microservice Architecture** 🏗  
  - **Stateless authentication** suitable for microservices  
  - **FastAPI** for high-performance, asynchronous processing  
  - **PostgreSQL** for user data persistence  
  - **Alembic** for database migrations  
  
- **Security Best Practices** ✅  
  - **BCrypt** for password hashing  
  - **Pydantic** for request validation  
  - **OAuth2-compatible login flow**  
  
- **Email Confirmation** ✉️  
  - **Celery** for background email processing  
  - **Redis** as a message broker for Celery  
  - **SMTP** integration to send email confirmation links  
  
## **📦 Tech Stack**  
| Technology  | Purpose |  
|-------------|---------|  
| **FastAPI**  | High-performance Python web framework |  
| **PostgreSQL**  | Database for user storage |  
| **SQLAlchemy**  | ORM for database interactions |  
| **Alembic**  | Database migrations |  
| **JWT (RS256)**  | Secure token-based authentication |  
| **BCrypt**  | Password hashing |  
| **Pydantic**  | Data validation and serialization |  
| **Celery**  | Task queue for email processing |  
| **Redis**  | Broker for Celery |

## **🔧 Setup & Run Locally**  

### **1️⃣ Clone the repository**  
```bash
git clone https://github.com/yourusername/auth-microservice.git
cd auth-microservice
```

### **2️⃣ Create a virtual environment**  
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### **3️⃣ Install dependencies**  
```bash
pip install -r requirements.txt
```

### **4️⃣ Configure `.env` file**  
Create a `.env` file in the root directory (example for localhost dev):  
```env
DEBUG=True
SERVER=127.0.0.1
SERVER_PORT=8000

DB_HOST=localhost
DB_PORT=5432
DB_NAME=auth_db
DB_USER=auth_service_user
DB_PASSWORD=admin

CELERY_BROKER_URL=redis://localhost:6379/0
SMTP_SERVER=your_smtp_server
SMTP_PORT=your_smtp_port
SMTP_FROM=your_email
SMTP_USERNAME=your_smtp_username
SMTP_PASSWORD=your_smtp_password

PRIVATE_KEY="-----BEGIN PRIVATE KEY-----...-----END PRIVATE KEY-----"
PUBLIC_KEY="-----BEGIN PUBLIC KEY-----...-----END PUBLIC KEY-----"

JWT_ALGORITHM=RS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### **5️⃣ Run database migrations**  
```bash
alembic upgrade head
```

### **6️⃣ Start the FastAPI server**  
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### **7️⃣ Start Celery Worker**  
```bash
celery -A app.celery worker --loglevel=info
```

### **8️⃣ Start Redis (If not running already)**  
```bash
redis-server
```

## **📌 Future Enhancements**  
- Add **rate limiting** to prevent brute force attacks  
- Implement **multi-factor authentication (MFA)**  
- Support for **role-based access control (RBAC)**  
- Expand third-party authentication (Google, Apple, GitHub, Facebook, etc.)  

## **🛠 Contributing**  
Oleksandr Kamenskyi

---
# Others

## DB
- `psql postgres`
- `CREATE DATABASE auth_db;`
- `CREATE USER auth_user WITH PASSWORD 'your_secure_password';`
- `GRANT ALL PRIVILEGES ON DATABASE auth_db TO auth_user;`
- `\q`

## Public / Private keys
- Private: `openssl genrsa -out private.pem 2048`
- Public, based on private: `openssl rsa -in private.pem -pubout -out public.pem`

## Alembic
- Init: `alembic init alembic`
- Make migrations: `alembic revision --autogenerate -m "COMMENT"`
- Migrate: `alembic upgrade head`

## Usage

### Verify JWT by Other Services in Python
```
import jwt
from fastapi import HTTPException

public_key = """-----BEGIN PUBLIC KEY-----\n<Your Public Key Here>\n-----END PUBLIC KEY-----"""

def verify_access_token(token: str):
    try:
        # Decode and verify the token using the public key
        decoded_token = jwt.decode(token, public_key, algorithms=["RS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

decoded_token = verify_access_token(token)
```

### Use with React Native
1. `npm install axios react-native-keychain`

2. ```
   import * as Keychain from 'react-native-keychain';
   
   // Save tokens securely in keychain
   async function saveTokens(accessToken, refreshToken) {
     await Keychain.setGenericPassword('access_token', accessToken);
     await Keychain.setGenericPassword('refresh_token', refreshToken);
   }
   
   // Retrieve tokens from keychain
   async function getTokens() {
     const accessToken = await Keychain.getGenericPassword('access_token');
     const refreshToken = await Keychain.getGenericPassword('refresh_token');
     return { accessToken, refreshToken };
   } 