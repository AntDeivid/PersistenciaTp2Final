import logging
from datetime import datetime, timedelta
from sqlite3 import IntegrityError
from typing import Optional

from sqlalchemy.orm import joinedload
from sqlmodel import extract

from src.app.core.db.database import get_db
from src.app.models.PaginationResult import PaginationResult
from src.app.models.contrato import Contrato
from src.app.models.pagamento import Pagamento
from src.app.models.usuario import Usuario
from src.app.models.veiculo import Veiculo


class ContratoRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create(self, contrato: Contrato) -> Contrato:
        try:
            with next(get_db()) as db:
                db.add(contrato)
                db.commit()
                db.refresh(contrato)
                self.logger.info("Contrato criado com sucesso!")
                return contrato
        except IntegrityError:
            self.logger.error("Erro ao criar contrato!")
            raise ValueError("Erro ao criar contrato!")

    def get_all_no_pagination(self) -> list[Contrato]:
        with next(get_db()) as db:
            self.logger.info("Buscando todos os contratos, sem paginação")
            return db.query(Contrato).all()

    def get_all(self, data_inicial: Optional[datetime] = None, data_final: Optional[datetime] = None, page: Optional[int] = 1, limit: Optional[int] = 10) -> list[Contrato]:
        with next(get_db()) as db:
            query = db.query(Contrato)
            if data_inicial and data_final:
                query = query.filter(Contrato.data_inicio >= data_inicial, Contrato.data_fim <= data_final)
            if data_inicial:
                query = query.filter(Contrato.data_inicio == data_inicial)
            self.logger.info(f"Buscando contratos com data inicial {data_inicial} e data final {data_final}")

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

    def get_by_id(self, contrato_id: int) -> Contrato:
        with next(get_db()) as db:
            self.logger.info(f"Buscando contrato de id {contrato_id}")
            return db.query(Contrato).filter(Contrato.id == contrato_id).first()

    def get_contratos_by_usuario_veiculo(self) -> list[Contrato]:
        with next(get_db()) as db:
            self.logger.info("Buscando todos os contratos com usuario e veiculo")
            return db.query(Contrato).options(joinedload(Contrato.usuario), joinedload(Contrato.veiculo)).all()

    def get_contratos_by_usuario_id(self, usuario_id: int) -> list[Contrato]:
        with next(get_db()) as db:
            self.logger.info(f"Buscando todos os contratos com usuario de id {usuario_id}")
            return db.query(Contrato).filter(Contrato.usuario_id == usuario_id).options(joinedload(Contrato.usuario), joinedload(Contrato.veiculo)).all()

    def get_contratos_by_veiculo_marca_pagamento_pago(self, veiculo_marca: str, pagamento_pago: Optional[bool] = None) -> list[Contrato]:
        with next(get_db()) as db:
            self.logger.info(f"Buscando todos os contratos com veiculo de marca {veiculo_marca} e pagamento pago {pagamento_pago}")
            if pagamento_pago is None:
                return db.query(Contrato).filter(Contrato.veiculo.has(marca=veiculo_marca)).options(joinedload(Contrato.veiculo), joinedload(Contrato.pagamento)).all()
            return db.query(Contrato).filter(Contrato.veiculo.has(marca=veiculo_marca), Contrato.pagamento.has(pago=pagamento_pago)).options(joinedload(Contrato.veiculo), joinedload(Contrato.pagamento)).all()

    def get_contratos_by_pagamento_vencimento_month_and_usuario_id(self, vencimento_month: datetime, usuario_id: Optional[int] = None) -> list[Contrato]:
        with next(get_db()) as db:
            vencimento_inicio = vencimento_month.replace(day=1)
            vencimento_fim = (vencimento_inicio + timedelta(days=31)).replace(day=1)

            query = db.query(Contrato).join(Pagamento).filter(
                Pagamento.vencimento >= vencimento_inicio,
                Pagamento.vencimento < vencimento_fim
            )#.options(joinedload(Contrato.pagamento))
            if usuario_id:
                query = query.filter(Contrato.usuario_id == usuario_id).options(joinedload(Contrato.usuario))
            self.logger.info(f"Buscando todos os contratos com pagamento de vencimento no mes {vencimento_month.month} e ano {vencimento_month.year}")
            return query.all()

    def get_quantidade_contratos(self) -> int:
        with next(get_db()) as db:
            self.logger.info("Buscando quantidade de contratos")
            return db.query(Contrato).count()

    def search(self, placa: Optional[str] = None, nome_usuario: Optional[str] = None, page: Optional[int] = 1, limit: Optional[int] = 10) -> list[Contrato]:
        with next(get_db()) as db:
            query = db.query(Contrato).join(Usuario).join(Veiculo)
            if placa:
                query = query.filter(Veiculo.placa.ilike(f"%{placa}%"))
            if nome_usuario:
                query = query.filter(Usuario.nome.ilike(f"%{nome_usuario}%"))

            self.logger.info(f"Buscando contratos com filtro placa={placa} e nome_usuario={nome_usuario}")

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

    def update(self, contrato_id: int, contrato_data: dict) -> Contrato:
        with next(get_db()) as db:
            contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
            if not contrato:
                return None
            for key, value in contrato_data.items():
                if hasattr(contrato, key):
                    setattr(contrato, key, value)
            db.commit()
            db.refresh(contrato)
            self.logger.info(f"Contrato de id {contrato_id} atualizado")
            return contrato

    def delete(self, contrato_id: int) -> bool:
        with next(get_db()) as db:
            contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
            if not contrato:
                return False
            db.delete(contrato)
            db.commit()
            self.logger.info(f"Contrato de id {contrato_id} deletado")
            return True