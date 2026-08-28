import secrets

from http import HTTPStatus
from typing import Annotated


from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api_intelbras.database.session import get_session
from api_intelbras.models.user import User
from api_intelbras.models.apikey import ApiKey
from api_intelbras.schemas.apikey import (
    ApiKeyCreate,
    ApiKeyOut

)
from api_intelbras.core.security import get_password_hash
from api_intelbras.core.token import get_current_user , is_admin

router = APIRouter(prefix='/credencial', tags=['credencial'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
IsAdmin = Annotated[User, Depends(is_admin)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=ApiKeyOut)
async def create_apikey(apikey: ApiKeyCreate, 
                      session: Session,
                      current_user: CurrentUser
                      ):
    
    api_key = secrets.token_hex(32)

    db_key = await session.scalar(
        select(ApiKey).where(
            (ApiKey.chave == api_key) 
        )
    )

    if db_key:
        if db_key.chave == api_key:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Erro interno, tente novamente.',
            )


    db_key = ApiKey(
        nome=apikey.nome,
        chave=api_key,
        ativo=True,
        user_id= current_user.id
    )

    session.add(db_key)
    await session.commit()
    await session.refresh(db_key)

    return db_key

"""
@router.get('/', response_model=UserList)
async def read_users(
    session: Session, 
    filter_users: Annotated[FilterPage, Query()],
    isadmin: IsAdmin

):
    query = await session.scalars(
        select(User).offset(filter_users.offset).limit(filter_users.limit)
    )

    users = query.all()

    return {'users': users}


@router.put('/{user_id}', response_model=UserPublic)
async def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser
):
    if current_user.id != user_id or current_user.role != "admin":
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    try:
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email
        await session.commit()
        await session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@router.delete('/{user_id}', response_model=Message)
async def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id or current_user.role != 'admin':
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    await session.delete(current_user)
    await session.commit()

    return {'message': 'User deleted'}
    """