import enum
from typing import List , Optional

from datetime import datetime
from sqlalchemy import func , Enum , JSON , ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api_intelbras.database.database import table_registry  

from api_intelbras.models.user import User



@table_registry.mapped_as_dataclass
class ApiKey:
    __tablename__ = "api_keys"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    chave: Mapped[str] = mapped_column(unique=True)
    ativo: Mapped[bool] = mapped_column(default=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="api_keys")
