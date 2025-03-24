import os
import logging
from termcolor import colored
from dotenv import load_dotenv

load_dotenv()

"""
# Logger
"""
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'magenta',
    }

    def format(self, record):
        log_message = super().format(record)
        return colored(log_message, self.COLORS.get(record.levelname, 'white'))

def setup_logger():
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter('%(asctime)s - %(levelname)s: %(message)s'))

    logger.addHandler(console_handler)
    return logger

logger = setup_logger()

"""
# App
"""

DEBUG = os.getenv("DEBUG", False)
SERVER = os.getenv("SERVER", "127.0.0.1")
SERVER_PORT = os.getenv("SERVER_PORT", "8000")

"""
# Database configuration
"""
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "auth_db")
DB_USER = os.getenv("DB_USER", "auth_service_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

"""
# Email Configuration
"""
SMTP_SERVER = os.getenv("SMTP_SERVER", None)
SMTP_PORT = os.getenv("SMTP_PORT", None)
SMTP_FROM = os.getenv("SMTP_FROM", None)
SMTP_USERNAME = os.getenv("SMTP_USERNAME", None)
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", None)

"""
# Celery
"""
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379")

"""
# Security
"""
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "your_private_key_here")
PUBLIC_KEY = os.getenv("PUBLIC_KEY", "your_public_key_here")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "RS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
