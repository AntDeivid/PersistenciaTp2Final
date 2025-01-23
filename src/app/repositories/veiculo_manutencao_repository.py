import logging
from datetime import datetime
from sqlite3 import IntegrityError

from sqlalchemy import func

from src.app.core.db.database import get_db
from src.app.models.manutencao import Manutencao
from src.app.models.veiculo import Veiculo
from src.app.models.veiculo_manutencao import VeiculoManutencao


class VeiculoManutencaoRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create(self, veiculo_manutencao: VeiculoManutencao) -> VeiculoManutencao:
        try:
            with next(get_db()) as db:
                db.add(veiculo_manutencao)
                db.commit()
                db.refresh(veiculo_manutencao)
                self.logger.info("Veículo_manutencao criado com sucesso!")
                return veiculo_manutencao
        except IntegrityError:
            self.logger.error("Erro ao criar veículo_manutencao!")
            raise ValueError("Erro ao criar veículo_manutencao!")

    def get_all(self) -> list[VeiculoManutencao]:
        with next(get_db()) as db:
            self.logger.info("Buscando todos os veículos_manutencao")
            return db.query(VeiculoManutencao).all()

    def get_by_id(self, veiculo_manutencao_id: int) -> VeiculoManutencao:
        with next(get_db()) as db:
            self.logger.info(f"Bucando veículo_manutencao de id {veiculo_manutencao_id}")
            return db.query(VeiculoManutencao).filter(VeiculoManutencao.id == veiculo_manutencao_id).first()

    def get_total_custo_manutencao_por_marca(self) -> list:
        with next(get_db()) as db:
            self.logger.info("Buscando total de custo de manutenção por marca")
            return (
                db.query(
                    Veiculo.marca,
                    func.sum(Manutencao.custo).label("custo_total")
                )
                .join(VeiculoManutencao, VeiculoManutencao.veiculo_id == Veiculo.id)
                .join(Manutencao, Manutencao.id == VeiculoManutencao.manutencao_id)
                .group_by(Veiculo.marca)
                .order_by(func.sum(Manutencao.custo).desc())
                .all()
            )

    def get_veiculos_com_mais_manutencoes(self, start_date: datetime, end_date: datetime) -> list:
        with next(get_db()) as db:
            self.logger.info(f"Consultando veículos com mais manutenções entre {start_date} e {end_date}")
            return (
                db.query(
                    Veiculo.modelo,
                    Veiculo.marca,
                    func.count(VeiculoManutencao.id).label("num_manutencoes")
                )
                .join(VeiculoManutencao, Veiculo.id == VeiculoManutencao.veiculo_id)
                .join(Manutencao, VeiculoManutencao.manutencao_id == Manutencao.id)
                .filter(Manutencao.data >= start_date, Manutencao.data <= end_date)
                .group_by(Veiculo.id)
                .order_by(func.count(VeiculoManutencao.id).desc())
                .all()
            )

    def get_manutencao_mais_cara_por_veiculo(self) -> list:
        with next(get_db()) as db:
            self.logger.info("Consultando manutenção mais cara por veículo")
            subquery = (
                db.query(
                    VeiculoManutencao.veiculo_id,
                    func.max(Manutencao.custo).label("max_custo")
                )
                .join(Manutencao, VeiculoManutencao.manutencao_id == Manutencao.id)
                .group_by(VeiculoManutencao.veiculo_id)
                .subquery()
            )

            return (
                db.query(
                    Veiculo.modelo,
                    Veiculo.marca,
                    Manutencao.tipo_manutencao,
                    Manutencao.custo,
                    Manutencao.observacao
                )
                .join(VeiculoManutencao, Veiculo.id == VeiculoManutencao.veiculo_id)
                .join(Manutencao, VeiculoManutencao.manutencao_id == Manutencao.id)
                .join(subquery, (Veiculo.id == subquery.c.veiculo_id) & (Manutencao.custo == subquery.c.max_custo))
                .all()
            )

    def get_veiculos_com_maior_custo_manutencao(self) -> list:
        from sqlalchemy import func

        with next(get_db()) as db:
            self.logger.info("Consultando veículos com maior custo de manutenção acumulado")
            return (
                db.query(
                    Veiculo.modelo,
                    Veiculo.marca,
                    func.sum(Manutencao.custo).label("custo_total")
                )
                .join(VeiculoManutencao, Veiculo.id == VeiculoManutencao.veiculo_id)
                .join(Manutencao, VeiculoManutencao.manutencao_id == Manutencao.id)
                .group_by(Veiculo.id)
                .order_by(func.sum(Manutencao.custo).desc())
                .all()
            )

    def get_quantidade_veiculos_manutencao(self) -> int:
        with next(get_db()) as db:
            self.logger.info("Buscando quantidade de veículos_manutencao")
            return db.query(VeiculoManutencao).count()

    def update(self, veiculo_manutencao_id: int, veiculo_manutencao_data: dict) -> VeiculoManutencao:
        with next(get_db()) as db:
            veiculo_manutencao = db.query(VeiculoManutencao).filter(VeiculoManutencao.id == veiculo_manutencao_id).first()
            if not veiculo_manutencao:
                return None
            for key, value in veiculo_manutencao_data.items():
                if hasattr(veiculo_manutencao, key):
                    setattr(veiculo_manutencao, key, value)
            db.commit()
            db.refresh(veiculo_manutencao)
            self.logger.info(f"Veículo_manutencao de id {veiculo_manutencao_id} atualizado")
            return veiculo_manutencao

    def delete(self, veiculo_manutencao_id: int) -> bool:
        with next(get_db()) as db:
            veiculo_manutencao = db.query(VeiculoManutencao).filter(VeiculoManutencao.id == veiculo_manutencao_id).first()
            if not veiculo_manutencao:
                return False
            db.delete(veiculo_manutencao)
            db.commit()
            self.logger.info(f"Veículo_manutencao de id {veiculo_manutencao_id} deletado")
            return True