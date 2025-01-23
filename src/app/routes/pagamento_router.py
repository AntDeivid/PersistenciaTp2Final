from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Query, Path

from src.app.models.pagamento import Pagamento
from src.app.repositories.pagamento_repository import PagamentoRepository

pagamento_router = APIRouter(prefix="/api/pagamentos", tags=["Pagamentos"])

pagamento_repository = PagamentoRepository()


@pagamento_router.post("/", response_model=Pagamento, status_code=status.HTTP_201_CREATED)
def create_pagamento(pagamento: Pagamento):
    try:
        return pagamento_repository.create(pagamento)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@pagamento_router.get("/")
def get_pagamentos(
    data_inicial: Optional[datetime] = Query(None),
    data_final: Optional[datetime] = Query(None),
    pago: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    return pagamento_repository.get_all(data_inicial, data_final, pago, page, limit)


@pagamento_router.get("/all")
def get_all_pagamentos():
    return pagamento_repository.get_all_no_pagination()


@pagamento_router.get("/pendentes-por-usuario", response_model=List[dict])
def get_pagamentos_pendentes_por_usuario():
    pagamentos_pendentes = pagamento_repository.get_pagamentos_pendentes_por_usuario()
    return [{"nome": nome, "email": email, "total_pendente": total_pendente} for nome, email, total_pendente in pagamentos_pendentes]

@pagamento_router.get("/{pagamento_id}", response_model=Pagamento)
def get_pagamento_by_id(pagamento_id: int = Path(..., title="The ID of the pagamento to get")):
    pagamento = pagamento_repository.get_by_id(pagamento_id)
    if not pagamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pagamento não encontrado"
        )
    return pagamento


@pagamento_router.put("/{pagamento_id}", response_model=Pagamento)
def update_pagamento(pagamento_id: int, pagamento_data: dict):
    updated_pagamento = pagamento_repository.update(pagamento_id, pagamento_data)
    if not updated_pagamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pagamento não encontrado"
        )
    return updated_pagamento


@pagamento_router.delete("/{pagamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pagamento(pagamento_id: int):
    deleted = pagamento_repository.delete(pagamento_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pagamento não encontrado"
        )
    return None