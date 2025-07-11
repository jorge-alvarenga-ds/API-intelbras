from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from http import HTTPStatus

from jwt import DecodeError, ExpiredSignatureError, decode, encode
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from api_intelbras.core.settings import Settings
from api_intelbras.database.session import get_session
from api_intelbras.models.user import User  # ajuste conforme sua estrutura

from sqlalchemy.ext.asyncio import AsyncSession

settings = Settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

async def get_current_user(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        subject_email = payload.get('sub')
        if not subject_email:
            raise credentials_exception
    except (DecodeError, ExpiredSignatureError):
        raise credentials_exception

    result = await session.scalar(
        select(User).where(User.email == subject_email)
    )
    if not result:
        raise credentials_exception

    return result
