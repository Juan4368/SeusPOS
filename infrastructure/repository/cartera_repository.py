from __future__ import annotations

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from domain.interfaces.cartera_repository import ICarteraRepository
from domain.models.entities.Cartera import Cartera
from domain.schemas.cartera import CarteraCreate
from infrastructure.database.models import Cartera as CarteraDB


class CarteraRepository(ICarteraRepository):
    """Implementación de repositorio de cartera utilizando SQLAlchemy."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, cartera: CarteraCreate) -> Cartera:
        db_cartera = CarteraDB(
            monto=cartera.monto,
            categoria_contabilidad_id=cartera.categoria_contabilidad_id,
            fecha=cartera.fecha,
            cliente=cartera.cliente,
            notas=cartera.notas,
        )

        try:
            self._db.add(db_cartera)
            self._db.commit()
            self._db.refresh(db_cartera)
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise exc

        return Cartera.model_validate(db_cartera)
