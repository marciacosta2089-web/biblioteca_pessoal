# app/main.py
from fastapi import FastAPI
from app.database import engine, Base
from app.routes import livros

# ⚙️ Import para o CORS dinâmico
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Biblioteca Pessoal API")

# 🔒 CORS configurável por variável de ambiente
origins = os.getenv("CORS_ORIGINS", "*")
allow_origins = [o.strip() for o in origins.split(",")] if origins else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🗃️ Criação das tabelas na primeira execução
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"mensagem": "Bem-vindo à API da Biblioteca Pessoal!"}

# 📚 Inclui as rotas dos livros
app.include_router(livros.router)
