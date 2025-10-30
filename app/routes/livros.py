# app/routes/livros.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models
from app.schemas import LivroCreate, LivroOut, LivroUpdate

router = APIRouter(prefix="/livros", tags=["livros"])

@router.get("", response_model=List[LivroOut])
def listar_livros(lista: str | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Livro)
    if lista in ("meus", "comprar"):
        query = query.filter(models.Livro.lista == lista)
    return query.order_by(models.Livro.id.desc()).all()

@router.post("", response_model=LivroOut, status_code=status.HTTP_201_CREATED)
def criar_livro(payload: LivroCreate, db: Session = Depends(get_db)):
    livro = models.Livro(
        nome=payload.nome,
        autor=payload.autor,
        classificacao=payload.classificacao,
        recomendado_por=payload.recomendado_por,
        lista=payload.lista,
    )
    db.add(livro)
    db.commit()
    db.refresh(livro)
    return livro

@router.put("/{livro_id}", response_model=LivroOut)
def atualizar_livro(livro_id: int, payload: LivroUpdate, db: Session = Depends(get_db)):
    livro = db.get(models.Livro, livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    for campo, valor in payload.model_dump(exclude_unset=True).items():
        setattr(livro, campo, valor)
    db.commit()
    db.refresh(livro)
    return livro

@router.delete("/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
def apagar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.get(models.Livro, livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db.delete(livro)
    db.commit()
    return

@router.post("/{livro_id}/mover", response_model=LivroOut)
def mover_livro(livro_id: int, destino: str, db: Session = Depends(get_db)):
    if destino not in ("meus", "comprar"):
        raise HTTPException(status_code=400, detail="Destino inválido: use 'meus' ou 'comprar'.")
    livro = db.get(models.Livro, livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    livro.lista = destino
    db.commit()
    db.refresh(livro)
    return livro

# --- Export CSV ---
@router.get("/export.csv")
def exportar_csv(db: Session = Depends(get_db)):
    import csv, io
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["id", "nome", "autor", "classificacao", "recomendado_por", "lista"])
    for l in db.query(models.Livro).order_by(models.Livro.id.asc()).all():
        writer.writerow([l.id, l.nome, l.autor, l.classificacao, l.recomendado_por or "", l.lista])
    buffer.seek(0)
    from fastapi.responses import Response
    return Response(
        content=buffer.read(),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="livros.csv"'},
    )
