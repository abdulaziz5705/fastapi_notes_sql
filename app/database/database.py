from typing import Annotated
import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# PostgreSQL bazasiga ulanish uchun URL
#                         "postgresql://username:password@localhost/db_name"
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# Engine yaratish
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Sessiya yaratish
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base yaratish
Base = declarative_base()

# Sessiya ochish
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]