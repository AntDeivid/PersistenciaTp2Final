from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Query, Path

from src.app.models.manutencao import Manutencao
from src.app.repositories.manutencao_repository import ManutencaoRepository

manutencao_router = APIRouter(prefix="/api/manutencoes", tags=["Manutenções"])

manutencao_repository = ManutencaoRepository()

@manutencao_router.post("/", response_model=Manutencao, status_code=status.HTTP_201_CREATED)
def create_manutencao(manutencao: Manutencao):
    try:
        return manutencao_repository.create(manutencao)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@manutencao_router.get("/")
def get_manutencoes(
    data_inicial: Optional[datetime] = Query(None),
    data_final: Optional[datetime] = Query(None),
    tipo_manutencao: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    return manutencao_repository.get_all(data_inicial, data_final, tipo_manutencao, page, limit)

@manutencao_router.get("/all")
def get_all_manutencoes():
    return manutencao_repository.get_all_no_pagination()


@manutencao_router.get("/total", response_model=int)
def get_total_manutencoes():
    return manutencao_repository.get_quantidade_manutencoes()


@manutencao_router.get("/tipos-frequentes", response_model=List[dict])
def get_tipos_manutencao_frequentes():
    tipos_frequentes = manutencao_repository.get_tipos_manutencao_mais_frequentes()
    return [{"tipo_manutencao": tipo, "frequencia": frequencia} for tipo, frequencia in tipos_frequentes]


@manutencao_router.get("/{manutencao_id}", response_model=Manutencao)
def get_manutencao_by_id(manutencao_id: int = Path(..., title="The ID of the manutencao to get")):
    manutencao = manutencao_repository.get_by_id(manutencao_id)
    if not manutencao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manutenção não encontrada")
    return manutencao

@manutencao_router.put("/{manutencao_id}", response_model=Manutencao)
def update_manutencao(manutencao_id: int, manutencao_data: dict):
    updated_manutencao = manutencao_repository.update(manutencao_id, manutencao_data)
    if not updated_manutencao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manutenção não encontrada")
    return updated_manutencao

@manutencao_router.delete("/{manutencao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_manutencao(manutencao_id: int):
    deleted = manutencao_repository.delete(manutencao_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manutenção não encontrada")
    return None