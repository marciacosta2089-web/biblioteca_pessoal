# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pathlib import Path
import os

class Base(DeclarativeBase):
    pass

# Se existir DATABASE_URL no ambiente (ex.: Render), usa-a.
env_db = os.getenv("DATABASE_URL")

if env_db:
    DATABASE_URL = env_db
    # Para SQLite, convém permitir threads
    connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
else:
    # Caminho absoluto dentro do projeto
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_DIR = BASE_DIR / "data"
    DB_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH = DB_DIR / "biblioteca.db"
    DATABASE_URL = f"sqlite:///{DB_PATH}"
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, echo=False, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
