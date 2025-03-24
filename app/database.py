from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session  # Make sure Session is imported
from .models import Base
from .config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
import psycopg2
from psycopg2 import sql
from .config import DATABASE_URL, logger


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_url = DATABASE_URL
db_url_parts = db_url.split("/")
db_name = db_url_parts[-1]
db_url_base = "/".join(db_url_parts[:-1])


def create_database():
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            dbname='postgres',  # Connect to the 'postgres' database to create a new one
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if the target database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            logger.warning(f"Database '{db_name}' created successfully.")
        else:
            logger.info(f"Database '{db_name}' already exists.")
    except Exception as e:
        logger.error(f"Error creating database: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """Database session generator"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


create_database()  # Creates the database if it doesn't exist
create_tables()  # Creates the tables based on models