from __future__ import annotations

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from domain.interfaces.egreso_repository import IEgresoRepository
from domain.models.entities.Egreso import Egreso
from domain.schemas.egreso import EgresoCreate
from infrastructure.database.models import Egreso as EgresoDB


class EgresoRepository(IEgresoRepository):
    """Implementación de repositorio de egresos utilizando SQLAlchemy."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, egreso: EgresoCreate) -> Egreso:
        db_egreso = EgresoDB(
            monto=egreso.monto,
            categoria_contabilidad_id=egreso.categoria_contabilidad_id,
            fecha=egreso.fecha,
            notas=egreso.notas,
            cliente=egreso.cliente,
            tipo_egreso=egreso.tipo_egreso,
        )

        try:
            self._db.add(db_egreso)
            self._db.commit()
            self._db.refresh(db_egreso)
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise exc

        return Egreso.model_validate(db_egreso)
