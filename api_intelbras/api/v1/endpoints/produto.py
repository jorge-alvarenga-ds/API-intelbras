from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_intelbras.database.session import get_session
from api_intelbras.models.produto import Produto
from api_intelbras.models.user import User
from api_intelbras.schemas.produto import (
                    ProdutoSchema , 
                    ProdutoUpDate ,
                    ListaProdutos,
                    FiltroProdutos,
                    Message)
from api_intelbras.core.token import get_current_user

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter()


@router.post('/', response_model=ProdutoSchema)
async def create_todo(
    produto: ProdutoSchema,
    user: CurrentUser,
    session: Session,
        ):
    
    db_produto = await session.scalar(
            select(Produto).where(
                (Produto.Produto == produto.produto)))
    
    if db_produto:
        if db_produto.Produto == produto.produto:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Produto Já existe',
            )


    db_produto = Produto(
                    Produto = produto.produto ,
                    Link_Produto = produto.link_produto ,
                    Titulo = produto.titulo ,
                    Descricao = produto.descricao ,
                    Imagens = produto.imagens ,
                    Beneficios = produto.beneficios ,
                    link_datasheet = produto.link_datasheet ,
                    Manual = produto.manual
        )
    session.add(db_produto)
    await session.commit()
    await session.refresh(db_produto)

    return db_produto


@router.get('/', response_model=ListaProdutos)
async def list_produtos(
    session: Session,
    user: CurrentUser,
    produto_filter: Annotated[FiltroProdutos, Query()],
):
    query = select(Produto)

    if produto_filter.produto:
        query = query.filter(Produto.Produto.contains(produto_filter.produto))

    produtos = await session.scalars(
        query.offset(produto_filter.offset).limit(produto_filter.limit)
    )

    return {"produtos": produtos.all()}


@router.patch('/{produto_id}', response_model=ProdutoSchema)
async def patch_produto(
    produto_id: str, session: Session, user: CurrentUser, produto: ProdutoUpDate
):
    db_produto = await session.scalar(
        select(Produto).where(Produto.Produto == produto_id)
    )

    if not db_produto:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Produto não encontrado.'
        )

    for key, value in produto.model_dump(exclude_unset=True).items():
        setattr(db_produto, key, value)
    session.add(db_produto)
    await session.commit()
    await session.refresh(db_produto)

    return db_produto


@router.delete('/{produto_id}', response_model=Message)
async def delete_todo(produto_id: str, session: Session, user: CurrentUser):
    db_produto = await session.scalar(
        select(Produto).where(Produto.Produto == produto_id)
    )

    if not db_produto:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Produto não encontrado.'
        )

    await session.delete(db_produto)
    await session.commit()

    return {'message': 'Produto deletado com sucesso.'}
    