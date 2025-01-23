from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship

from src.app.models.pagamento import Pagamento
from src.app.models.veiculo import Veiculo

class Contrato(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True, nullable=False)
    usuario_id: int = Field(foreign_key="usuario.id", nullable=False)
    veiculo_id: int = Field(foreign_key="veiculo.id", nullable=False)
    pagamento_id: int = Field(foreign_key="pagamento.id", nullable=True)
    data_inicio: datetime = Field(nullable=False)
    data_fim: datetime = Field(nullable=False)

    usuario: Optional["Usuario"] = Relationship(back_populates="contratos")
    veiculo: Optional[Veiculo] = Relationship(back_populates="contratos")
    pagamento: Optional[Pagamento] = Relationship(sa_relationship_kwargs={"uselist": False}, back_populates="contrato")

    class Config:
        orm_mode = True