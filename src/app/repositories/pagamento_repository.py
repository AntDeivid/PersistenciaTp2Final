import logging
from datetime import datetime
from sqlite3 import IntegrityError
from typing import Optional

from src.app.core.db.database import get_db
from src.app.models.PaginationResult import PaginationResult
from src.app.models.contrato import Contrato
from src.app.models.pagamento import Pagamento
from src.app.models.usuario import Usuario


class PagamentoRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create(self, pagamento: Pagamento) -> Pagamento:
        try:
            with next(get_db()) as db:
                db.add(pagamento)
                db.commit()
                db.refresh(pagamento)
                self.logger.info("Pagamento criado com sucesso!")
                return pagamento
        except IntegrityError:
            self.logger.error("Erro ao criar pagamento!")
            raise ValueError("Erro ao criar pagamento!")

    def get_all_no_pagination(self) -> list[Pagamento]:
        with next(get_db()) as db:
            self.logger.info("Buscando todos os pagamentos, sem paginação")
            return db.query(Pagamento).all()

    def get_all(
            self,
            data_inicial: Optional[datetime] = None,
            data_final: Optional[datetime] = None,
            pago: Optional[bool] = None,
            page: Optional[int] = 1,
            limit: Optional[int] = 10
    ):
        with next(get_db()) as db:
            query = db.query(Pagamento)
            if data_inicial and data_final:
                query = query.filter(Pagamento.vencimento >= data_inicial, Pagamento.vencimento <= data_final)
            if data_inicial:
                query = query.filter(Pagamento.vencimento == data_inicial)
            if pago is not None:
                query = query.filter(Pagamento.pago == pago)

            self.logger.info(f"Buscando pagamentos com filtros: data_inicial={data_inicial}, data_final={data_final}, pago={pago}")

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

    def get_by_id(self, pagamento_id: int) -> Pagamento:
        with next(get_db()) as db:
            self.logger.info(f"Buscando pagamento de id {pagamento_id}")
            return db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()

    def get_pagamentos_pendentes_por_usuario(self) -> list:
        from sqlalchemy import func

        with next(get_db()) as db:
            self.logger.info("Consultando pagamentos pendentes por usuário")
            return (
                db.query(
                    Usuario.nome,
                    Usuario.email,
                    func.sum(Pagamento.valor).label("total_pendente")
                )
                .join(Contrato, Usuario.id == Contrato.usuario_id)
                .join(Pagamento, Contrato.pagamento_id == Pagamento.id)
                .filter(Pagamento.pago == False)
                .group_by(Usuario.id)
                .order_by(func.sum(Pagamento.valor).desc())
                .all()
            )

    def update(self, pagamento_id: int, pagamento_data: dict) -> Pagamento:
        with next(get_db()) as db:
            pagamento = db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
            if not pagamento:
                return None
            for key, value in pagamento_data.items():
                if hasattr(pagamento, key):
                    setattr(pagamento, key, value)
            db.commit()
            db.refresh(pagamento)
            self.logger.info(f"Pagamento de id {pagamento_id} atualizado")
            return pagamento

    def delete(self, pagamento_id: int) -> bool:
        with next(get_db()) as db:
            pagamento = db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
            if not pagamento:
                return False
            db.delete(pagamento)
            db.commit()
            self.logger.info(f"Pagamento de id {pagamento_id} deletado")
            return True