from __future__ import annotations

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from domain.interfaces.ingreso_repository import IIngresoRepository
from domain.models.entities.Ingreso import Ingreso
from domain.schemas.ingreso import IngresoCreate
from infrastructure.database.models import Ingreso as IngresoDB


class IngresoRepository(IIngresoRepository):
    """Implementación de repositorio utilizando SQLAlchemy."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, ingreso: IngresoCreate) -> Ingreso:
        db_ingreso = IngresoDB(
            monto=ingreso.monto,
            categoria_contabilidad_id=ingreso.categoria_contabilidad_id,
            fecha=ingreso.fecha,
            notas=ingreso.notas,
            cliente=ingreso.cliente,
            tipo_ingreso=ingreso.tipo_ingreso,
        )

        try:
            self._db.add(db_ingreso)
            self._db.commit()
            self._db.refresh(db_ingreso)
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise exc

        return Ingreso.model_validate(db_ingreso)
