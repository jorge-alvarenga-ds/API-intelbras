from fastapi import FastAPI
from api_intelbras.core.settings import settings
from api_intelbras.api.v1.api import api_router

app = FastAPI(title='API Intelbras') # nome da api

app.include_router(api_router, prefix=settings.API_VERSION) # adicionamos as rotas e usamos a variavel de versão para escolher qual versão vai rodar

if __name__ == '__main__':

    import uvicorn

  
# definimos o servidor uvicorn para rodar aplicção
    uvicorn.run("main:app", host="0.0.0.0", port=8000, 
                og_level='info', reload=True)