from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# PostgreSQL connection string
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:Music$14@localhost:5432/nutrition_app"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()