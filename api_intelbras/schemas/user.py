from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Literal , Optional , List

class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Literal["admin", "user"] = "user"
    credenciais: Optional[List[str]] = []


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)
    role: Literal["admin", "user"] = "user"
    credenciais: Optional[List[str]] = []
    


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str
    


class FilterPage(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, ge=1)



