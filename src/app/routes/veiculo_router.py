from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Query, Path

from src.app.models.veiculo import Veiculo
from src.app.repositories.veiculo_repository import VeiculoRepository

veiculo_router = APIRouter(prefix="/api/veiculos", tags=["Veículos"])

veiculo_repository = VeiculoRepository()

@veiculo_router.post("/", response_model=Veiculo, status_code=status.HTTP_201_CREATED)
def create_veiculo(veiculo: Veiculo):
    try:
        return veiculo_repository.create(veiculo)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@veiculo_router.get("/")
def get_veiculos(
    tipo: Optional[str] = Query(None),
    marca: Optional[str] = Query(None),
    modelo: Optional[str] = Query(None),
    ano: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    return veiculo_repository.get_all(tipo, marca, modelo, ano, page, limit)


@veiculo_router.get("/all")
def get_all_veiculos():
    return veiculo_repository.get_all_no_pagination()


@veiculo_router.get("/total", response_model=int)
def get_total_veiculos():
    return veiculo_repository.get_quantidade_veiculos()


@veiculo_router.get("/com-manutencoes")
def get_veiculos_com_manutencoes():
    return veiculo_repository.get_veiculos_com_manutencoes()


@veiculo_router.get("/tipo-manutencao/{tipo_manutencao}")
def get_veiculos_by_tipo_manutencao(tipo_manutencao: str = Path(..., title="The type of maintenance to filter vehicles")):
    return veiculo_repository.get_veiculos_by_tipo_manutencao(tipo_manutencao)


@veiculo_router.get("/custo-medio-manutencoes", response_model=List[dict])
def get_custo_medio_manutencoes_por_veiculo():
    custos_medios = veiculo_repository.get_custo_medio_manutencoes_por_veiculo()
    return [{"modelo": modelo, "marca": marca, "custo_medio": custo_medio} for modelo, marca, custo_medio in custos_medios]

@veiculo_router.get("/{veiculo_id}", response_model=Veiculo)
def get_veiculo_by_id(veiculo_id: int = Path(..., title="The ID of the vehicle to get")):
    veiculo = veiculo_repository.get_by_id(veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veículo não encontrado")
    return veiculo


@veiculo_router.put("/{veiculo_id}", response_model=Veiculo)
def update_veiculo(veiculo_id: int, veiculo_data: dict):
    updated_veiculo = veiculo_repository.update(veiculo_id, veiculo_data)
    if not updated_veiculo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veículo não encontrado")
    return updated_veiculo


@veiculo_router.delete("/{veiculo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_veiculo(veiculo_id: int):
    deleted = veiculo_repository.delete(veiculo_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veículo não encontrado")
    return None