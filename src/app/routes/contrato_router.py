from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Query, Path
from pydantic import BaseModel

from src.app.models.contrato import Contrato
from src.app.repositories.contrato_repository import ContratoRepository

contrato_router = APIRouter(prefix="/api/contratos", tags=["Contratos"])

contrato_repository = ContratoRepository()


@contrato_router.post("/", response_model=Contrato, status_code=status.HTTP_201_CREATED)
def create_contrato(contrato: Contrato):
    try:
        return contrato_repository.create(contrato)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@contrato_router.get("/")
def get_contratos(
    data_inicial: Optional[datetime] = Query(None),
    data_final: Optional[datetime] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    return contrato_repository.get_all(data_inicial, data_final, page, limit)


@contrato_router.get("/all")
def get_all_contratos():
    return contrato_repository.get_all_no_pagination()


@contrato_router.get("/total", response_model=int)
def get_total_contratos():
    return contrato_repository.get_quantidade_contratos()


@contrato_router.get("/search")
def search_contratos(
    placa: Optional[str] = Query(None),
    nome_usuario: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    return contrato_repository.search(placa, nome_usuario, page, limit)


@contrato_router.get("/{contrato_id}", response_model=Contrato)
def get_contrato_by_id(contrato_id: int = Path(..., title="The ID of the contrato to get")):
    contrato = contrato_repository.get_by_id(contrato_id)
    if not contrato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contrato não encontrado"
        )
    return contrato


@contrato_router.get("/usuario-veiculo/")
def get_contratos_by_usuario_veiculo():
    return contrato_repository.get_contratos_by_usuario_veiculo()


@contrato_router.get("/usuario/{usuario_id}")
def get_contratos_by_usuario_id(
    usuario_id: int = Path(..., title="The ID of the user to get contracts")
):
    return contrato_repository.get_contratos_by_usuario_id(usuario_id)


@contrato_router.get("/veiculo/{veiculo_marca}")
def get_contratos_by_veiculo_marca(
    veiculo_marca: str = Path(
        ..., title="The brand of the vehicle to get contracts"
    ),
    pagamento_pago: Optional[bool] = Query(None),
):
    return contrato_repository.get_contratos_by_veiculo_marca_pagamento_pago(
        veiculo_marca, pagamento_pago
    )

@contrato_router.get("/pagamento/vencimento/{vencimento_month}")
def get_contratos_by_pagamento_vencimento_month(
    vencimento_month: datetime = Path(..., title="The month and year of the due date"),
    usuario_id: Optional[int] = Query(None),
):
    return contrato_repository.get_contratos_by_pagamento_vencimento_month_and_usuario_id(vencimento_month, usuario_id)


@contrato_router.put("/{contrato_id}", response_model=Contrato)
def update_contrato(contrato_id: int, contrato_data: dict):
    updated_contrato = contrato_repository.update(contrato_id, contrato_data)
    if not updated_contrato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contrato não encontrado"
        )
    return updated_contrato


@contrato_router.delete("/{contrato_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contrato(contrato_id: int):
    deleted = contrato_repository.delete(contrato_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contrato não encontrado"
        )
    return None