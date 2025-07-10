from fastapi import APIRouter # apirouter para adicionar as rotas
# Toda vez que adicionarmos uma nova rota temos que importa la aqui
from api_intelbras.api.v1.endpoints import usuario 


api_router = APIRouter() # inicia a api de rotas

api_router.include_router(usuario.router, 
				prefix='/usuario', # adiciona o prifixo todo os endpoints daquela rota
				tags=['usuario'],# agrupa todos os endpoints na tag que foi passada
				summary = "Parte para criação de usuarios para acessar api.",
				description = "Uma string mais longa que descreve a rota em detalhes. Pode usar Markdown. Aparece na documentação.",
				response_description=" (Opcional) Uma string que descreve o significado da resposta."
				 ) 				 
