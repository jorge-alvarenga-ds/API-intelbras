from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from fastapi import Depends

from api_intelbras.core.settings import settings

# Criação do engine
engine: AsyncEngine = create_async_engine(settings.DATABASE_URL, echo=True)

# Criação do sessionmaker
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Função para injetar sessão nas rotas com Depends
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
