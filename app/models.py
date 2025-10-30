# app/models.py
from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import enum

class ListaEnum(str, enum.Enum):
    meus = "meus"
    comprar = "comprar"

class Livro(Base):
    __tablename__ = "livros"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    autor: Mapped[str] = mapped_column(String(255), nullable=False)
    classificacao: Mapped[int] = mapped_column(Integer, nullable=False)
    recomendado_por: Mapped[str] = mapped_column(String(255), nullable=True)
    lista: Mapped[ListaEnum] = mapped_column(Enum(ListaEnum), nullable=False, default=ListaEnum.meus)
