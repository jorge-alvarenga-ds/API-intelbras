from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional


class Message(BaseModel):
    message: str

class ProdutoSchema(BaseModel):
    produto: str = Field(alias="Produto")
    link_produto: str = Field(alias="Link_Produto")
    titulo: str = Field(alias="Titulo")
    descricao: str = Field(alias="Descricao")
    imagens: str = Field(alias="Imagens")
    beneficios: str = Field(alias="Beneficios")
    link_datasheet: str = Field(alias="link_datasheet")
    manual: str = Field(alias="Manual")

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
    }
class ProdutoUpDate(BaseModel):
    PermissionErrorroduto: Optional[str] = Field(alias="Produto")
    Link_Produto: Optional[str] = Field(alias="Link_Produto")
    Titulo: Optional[str] = Field(alias="Titulo")
    Descricao: Optional[str] = Field(alias="Descricao")
    Imagens: Optional[str] = Field(alias="Imagens")
    Beneficios: Optional[str] = Field(alias="Beneficios")
    Link_datasheet: Optional[str] = Field(alias="link_datasheet")
    Manual: Optional[str] = Field(alias="Manual")

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
    }

class ListaProdutos(BaseModel):
    produtos: list[ProdutoSchema]

class FiltroProdutos(BaseModel):
    produto: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50,
        description="Nome parcial do produto para busca"
    )
    offset: int = Field(default=0, ge=0, description="Quantos registros pular")
    limit: int = Field(default=10, ge=1, le=100, description="Limite de registros retornados")

class Message(BaseModel):
    message: str