from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class Pagamento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True, nullable=False)
    valor: float = Field(nullable=False)
    forma_pagamento: str = Field(max_length=100, nullable=False)
    vencimento: datetime = Field(nullable=False)
    pago: bool = Field(default=False)

    contrato: Optional["Contrato"] = Relationship(back_populates="pagamento")

    class Config:
        orm_mode = True