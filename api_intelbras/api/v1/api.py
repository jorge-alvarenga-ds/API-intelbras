from fastapi import APIRouter # apirouter para adicionar as rotas
# Toda vez que adicionarmos uma nova rota temos que importa la aqui
from api_intelbras.api.v1.endpoints import auth 
from api_intelbras.api.v1.endpoints import users
from api_intelbras.api.v1.endpoints import produto


api_router = APIRouter() # inicia a api de rotas

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"]
)			 
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)	
api_router.include_router(
    produto.router,
    prefix="/produto",
    tags=["produto"]
)	