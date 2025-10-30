# app/schemas.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal

ListaLiteral = Literal["meus", "comprar"]

class LivroBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=255)
    autor: str = Field(..., min_length=1, max_length=255)
    classificacao: int = Field(..., description="Número natural entre 1 e 10")
    recomendado_por: Optional[str] = Field(None, max_length=255)
    lista: ListaLiteral = "meus"

    @field_validator("classificacao")
    @classmethod
    def validar_classificacao(cls, v: int) -> int:
        if not (1 <= v <= 10):
            raise ValueError("A classificação deve ser um inteiro entre 1 e 10.")
        return v

class LivroCreate(LivroBase):
    pass

class LivroUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=255)
    autor: Optional[str] = Field(None, min_length=1, max_length=255)
    classificacao: Optional[int] = None
    recomendado_por: Optional[str] = Field(None, max_length=255)
    lista: Optional[ListaLiteral] = None

    @field_validator("classificacao")
    @classmethod
    def validar_classificacao(cls, v):
        if v is None:
            return v
        if not (1 <= v <= 10):
            raise ValueError("A classificação deve ser um inteiro entre 1 e 10.")
        return v

class LivroOut(LivroBase):
    id: int

    class Config:
        from_attributes = True
