from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True, nullable=False)
    nome: str = Field(max_length=100, nullable=False)
    email: str = Field(max_length=100, nullable=False, unique=True)
    celular: Optional[str] = Field(default=None, max_length=20)
    cpf: str = Field(max_length=14, nullable=False, unique=True)
    # apelido: Optional[str] = Field(default=None, max_length=100)

    contratos: Optional["Contrato"] = Relationship(back_populates="usuario")

    class Config:
        orm_mode = True