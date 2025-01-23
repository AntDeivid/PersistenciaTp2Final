from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

from src.app.models.veiculo_manutencao import VeiculoManutencao


class Manutencao (SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True, nullable=False)
    data: datetime = Field(nullable=False)
    tipo_manutencao: str = Field(nullable=False)
    custo : float = Field(nullable=False)
    observacao: str = Field(nullable=False)

    veiculos: List["Veiculo"] = Relationship(
        back_populates="manutencoes", link_model=VeiculoManutencao
    )


    class Config:
        orm_mode = True
