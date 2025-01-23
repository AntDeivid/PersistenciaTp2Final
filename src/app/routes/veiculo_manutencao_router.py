from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Query, Path

from src.app.models.veiculo_manutencao import VeiculoManutencao
from src.app.repositories.veiculo_manutencao_repository import VeiculoManutencaoRepository

veiculo_manutencao_router = APIRouter(prefix="/api/veiculos-manutencao", tags=["Veículos-Manutenção"])

veiculo_manutencao_repository = VeiculoManutencaoRepository()


@veiculo_manutencao_router.post("/", response_model=VeiculoManutencao, status_code=status.HTTP_201_CREATED)
def create_veiculo_manutencao(veiculo_manutencao: VeiculoManutencao):
    try:
        return veiculo_manutencao_repository.create(veiculo_manutencao)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@veiculo_manutencao_router.get("/", response_model=List[VeiculoManutencao])
def get_veiculos_manutencao():
    return veiculo_manutencao_repository.get_all()


@veiculo_manutencao_router.get("/total", response_model=int)
def get_total_veiculos_manutencao():
    return veiculo_manutencao_repository.get_quantidade_veiculos_manutencao()


@veiculo_manutencao_router.get("/custo-por-marca", response_model=List[dict])
def get_total_custo_manutencao_por_marca():
    custos_por_marca = veiculo_manutencao_repository.get_total_custo_manutencao_por_marca()
    return [{"marca": marca, "custo_total": custo_total} for marca, custo_total in custos_por_marca]


@veiculo_manutencao_router.get("/mais-manutencoes", response_model=List[dict])
def get_veiculos_com_mais_manutencoes(start_date: datetime = Query(...), end_date: datetime = Query(...)):
    veiculos_manutencoes = veiculo_manutencao_repository.get_veiculos_com_mais_manutencoes(start_date, end_date)
    return [{"modelo": modelo, "marca": marca, "num_manutencoes": num_manutencoes} for modelo, marca, num_manutencoes in veiculos_manutencoes]


@veiculo_manutencao_router.get("/manutencao-mais-cara", response_model=List[dict])
def get_manutencao_mais_cara_por_veiculo():
    manutencoes_caras = veiculo_manutencao_repository.get_manutencao_mais_cara_por_veiculo()
    return [{"modelo": modelo, "marca": marca, "tipo_manutencao": tipo_manutencao, "custo": custo, "observacao": observacao} for modelo, marca, tipo_manutencao, custo, observacao in manutencoes_caras]


@veiculo_manutencao_router.get("/maior-custo-total", response_model=List[dict])
def get_veiculos_com_maior_custo_manutencao():
    veiculos_custos = veiculo_manutencao_repository.get_veiculos_com_maior_custo_manutencao()
    return [{"modelo": modelo, "marca": marca, "custo_total": custo_total} for modelo, marca, custo_total in veiculos_custos]


@veiculo_manutencao_router.get("/{veiculo_manutencao_id}", response_model=VeiculoManutencao)
def get_veiculo_manutencao_by_id(veiculo_manutencao_id: int = Path(..., title="The ID of the veiculo_manutencao to get")):
    veiculo_manutencao = veiculo_manutencao_repository.get_by_id(veiculo_manutencao_id)
    if not veiculo_manutencao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veículo-Manutenção não encontrado")
    return veiculo_manutencao


@veiculo_manutencao_router.put("/{veiculo_manutencao_id}", response_model=VeiculoManutencao)
def update_veiculo_manutencao(veiculo_manutencao_id: int, veiculo_manutencao_data: dict):
    updated_veiculo_manutencao = veiculo_manutencao_repository.update(veiculo_manutencao_id, veiculo_manutencao_data)
    if not updated_veiculo_manutencao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veículo-Manutenção não encontrado")
    return updated_veiculo_manutencao


@veiculo_manutencao_router.delete("/{veiculo_manutencao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_veiculo_manutencao(veiculo_manutencao_id: int):
    deleted = veiculo_manutencao_repository.delete(veiculo_manutencao_id)
    if not deleted:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veículo-Manutenção não encontrado")
    return None