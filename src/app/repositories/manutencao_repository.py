import logging
from datetime import datetime
from sqlite3 import IntegrityError
from typing import Optional

from src.app.core.db.database import get_db
from src.app.models.PaginationResult import PaginationResult
from src.app.models.manutencao import Manutencao


class ManutencaoRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create(self, manutencao: Manutencao) -> Manutencao:
        try:
            with next(get_db()) as db:
                db.add(manutencao)
                db.commit()
                db.refresh(manutencao)
                self.logger.info("Manutenção criada com sucesso!")
                return manutencao
        except IntegrityError:
            self.logger.error("Erro ao criar manutenção!")
            raise ValueError("Erro ao criar manutenção!")

    def get_all_no_pagination(self) -> list[Manutencao]:
        with next(get_db()) as db:
            self.logger.info("Buscando todas as manutenções, sem paginação")
            return db.query(Manutencao).all()

    def get_all(
            self,
            data_inicial: Optional[datetime] = None,
            data_final: Optional[datetime] = None,
            tipo_manutencao: Optional[str] = None,
            page: Optional[int] = 1,
            limit: Optional[int] = 10
    ) -> list[Manutencao]:
        with next(get_db()) as db:
            query = db.query(Manutencao)
            if data_inicial and data_final:
                query = query.filter(Manutencao.data >= data_inicial, Manutencao.data <= data_final)
            elif data_inicial:
                query = query.filter(Manutencao.data == data_inicial)
            if tipo_manutencao:
                query = query.filter(Manutencao.tipo_manutencao == tipo_manutencao)

            self.logger.info("Buscando todas as manutenções")

            total_items = query.count()
            number_of_pages = total_items // limit if total_items % limit == 0 else (total_items // limit) + 1
            data = query.offset((page - 1) * limit).limit(limit).all()

            return PaginationResult(
                page=page,
                limit=limit,
                total_items=total_items,
                number_of_pages=number_of_pages,
                data=data
            )

    def get_by_id(self, manutencao_id: int) -> Manutencao:
        with next(get_db()) as db:
            self.logger.info(f"Buscando manutenção de id {manutencao_id}")
            return db.query(Manutencao).filter(Manutencao.id == manutencao_id).first()

    def get_tipos_manutencao_mais_frequentes(self) -> list:
        from sqlalchemy import func

        with next(get_db()) as db:
            self.logger.info("Consultando tipos de manutenção mais frequentes")
            return (
                db.query(
                    Manutencao.tipo_manutencao,
                    func.count(Manutencao.id).label("frequencia")
                )
                .group_by(Manutencao.tipo_manutencao)
                .order_by(func.count(Manutencao.id).desc())
                .all()
            )

    def get_quantidade_manutencoes(self) -> int:
        with next(get_db()) as db:
            self.logger.info("Buscando quantidade de manutenções")
            return db.query(Manutencao).count()

    def update(self, manutencao_id: int, manutencao_data: dict) -> Manutencao:
        with next(get_db()) as db:
            manutencao = db.query(Manutencao).filter(Manutencao.id == manutencao_id).first()
            if not manutencao:
                return None
            for key, value in manutencao_data.items():
                if hasattr(manutencao, key):
                    setattr(manutencao, key, value)
            db.commit()
            db.refresh(manutencao)
            self.logger.info(f"Manutenção de id {manutencao_id} atualizada")
            return manutencao

    def delete(self, manutencao_id: int) -> bool:
        with next(get_db()) as db:
            manutencao = db.query(Manutencao).filter(Manutencao.id == manutencao_id).first()
            if not manutencao:
                return False
            db.delete(manutencao)
            db.commit()
            self.logger.info(f"Manutenção de id {manutencao_id} deletada")
            return True