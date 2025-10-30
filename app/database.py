# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from pathlib import Path

# Base do projeto (…/src)
BASE_DIR = Path(__file__).resolve().parent.parent

# Garante que a pasta data/ existe (Render permite escrita no /opt/render/project/src)
DB_DIR = BASE_DIR / "data"
DB_DIR.mkdir(parents=True, exist_ok=True)

# Caminho absoluto para o ficheiro SQLite
DB_PATH = DB_DIR / "biblioteca.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Para SQLite + FastAPI, activa connect_args
engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
