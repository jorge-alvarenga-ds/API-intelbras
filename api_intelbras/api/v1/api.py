from fastapi import APIRouter # apirouter para adicionar as rotas
# Toda vez que adicionarmos uma nova rota temos que importa la aqui
from api_intelbras.api.v1.endpoints import auth 


api_router = APIRouter() # inicia a api de rotas

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"]
)			 
