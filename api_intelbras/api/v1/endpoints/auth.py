from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Defina com o nome do projeot
from api_intelbras.database.session import get_session
from api_intelbras.models.user import User
from api_intelbras.schemas.auth import Token
from api_intelbras.core.security import verify_password
from api_intelbras.core.token import(
                            create_access_token,
                            get_current_user,
                            )

router = APIRouter()
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[AsyncSession, Depends(get_session)]

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2Form, 
                                 session: Session):
    user = await session.scalar(select(User).where(User.email == form_data.username))
    if form_data.grant_type == "password":
        if not user:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Usuário ou senha incorreto.',
            )
        if not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Usuário ou senha incorreto.',
            )
    if form_data.grant_type == "client_credentials":
        if not user:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Usuário ou Credencial incorreto.',
            )
        credenciais =user.credenciais or []
        if not form_data.client_secret in credenciais:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Usuário ou Credencial incorreto.',
            )
        
    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}

  
@router.post('/refresh_token', response_model=Token)
async def refresh_access_token(
    user: User = Depends(get_current_user),
):
    new_access_token = create_access_token(data={'sub': user.email})
    return {'access_token': new_access_token, 'token_type': 'bearer'}