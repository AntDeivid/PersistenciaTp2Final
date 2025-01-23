from typing import Optional
from sqlmodel import SQLModel, Field

class VeiculoManutencao(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True, nullable=False)
    veiculo_id: int = Field(nullable=False, foreign_key="veiculo.id")
    manutencao_id: int = Field(nullable=False, foreign_key="manutencao.id")

    class Config:
        orm_mode = True
