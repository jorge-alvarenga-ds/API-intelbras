from pydantic import BaseModel, Field
from typing import  Optional , List


class ApiKeyCreate(BaseModel):
    nome: str


class ApiKeyOut(BaseModel):
    id: int
    nome: str
    chave: str
    ativo: bool
