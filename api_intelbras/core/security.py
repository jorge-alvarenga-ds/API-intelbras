from pwdlib import PasswordHash

from api_intelbras.core.settings import Settings

settings = Settings()
pwd_context = PasswordHash.recommended()

# Função para gerar o hash da senha para armazenar no banco de dados
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Função para verificar se a senha corresponde ao hash
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)