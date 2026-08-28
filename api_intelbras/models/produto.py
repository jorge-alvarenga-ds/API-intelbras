from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api_intelbras.database.database import table_registry  

@table_registry.mapped_as_dataclass
class Produto:
    __tablename__ = 'produto'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    Produto: Mapped[str] = mapped_column(unique=True)

    Link_Produto: Mapped[str] = mapped_column()

    Titulo: Mapped[str] = mapped_column()

    Descricao: Mapped[str] = mapped_column()

    Imagens: Mapped[str] = mapped_column()

    Beneficios: Mapped[str] = mapped_column()

    link_datasheet: Mapped[str] = mapped_column()

    Manual: Mapped[str] = mapped_column()


    created_at: Mapped[datetime] = mapped_column(
            init=False, server_default=func.now()
            )

    updated_at: Mapped[datetime] = mapped_column(
            init=False, server_default=func.now(), onupdate=func.now()
            )