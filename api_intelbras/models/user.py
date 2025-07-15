import enum
from typing import List , Optional

from datetime import datetime
from sqlalchemy import func , Enum , JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api_intelbras.database.database import table_registry  

from api_intelbras.models.apikey import ApiKey


class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"   

@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    username: Mapped[str] = mapped_column(unique=True)

    password: Mapped[str]

    email: Mapped[str] = mapped_column(unique=True)
    
    role: Mapped[RoleEnum] = mapped_column(
                                Enum(RoleEnum), default=RoleEnum.user
                                )
    api_keys: Mapped[List["ApiKey"]] = relationship(back_populates="user")

    created_at: Mapped[datetime] = mapped_column(
            init=False, server_default=func.now()
            )

    updated_at: Mapped[datetime] = mapped_column(
            init=False, server_default=func.now(), onupdate=func.now()
            )