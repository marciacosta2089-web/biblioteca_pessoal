# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import livros

app = FastAPI(title="Biblioteca Pessoal API")

# CORS (ajuda quando criares um frontend separado)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restringe futuramente p/ produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria as tabelas na primeira execução
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"mensagem": "Bem-vindo à API da Biblioteca Pessoal!"}

app.include_router(livros.router)
