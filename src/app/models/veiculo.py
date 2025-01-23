from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from src.app.models.veiculo_manutencao import VeiculoManutencao


class Veiculo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True, nullable=False)
    modelo: str = Field(max_length=100, nullable=False)
    marca: str = Field(max_length=100, nullable=False)
    placa: str = Field(max_length=7, nullable=False, unique=True)
    ano: int = Field(nullable=False)

    contratos: Optional["Contrato"] = Relationship(back_populates="veiculo")
    manutencoes: List["Manutencao"] = Relationship(
        back_populates="veiculos", link_model=VeiculoManutencao
    )

    class Config:
        orm_mode = True