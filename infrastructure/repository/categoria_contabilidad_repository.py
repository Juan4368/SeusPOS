from __future__ import annotations

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from domain.interfaces.categoria_contabilidad_repository import (
    ICategoriaContabilidadRepository,
)
from domain.models.entities.CategoriaContabilidad import CategoriaContabilidad
from domain.schemas.categoria_contabilidad import CategoriaContabilidadCreate
from infrastructure.database.models import CategoriaContabilidad as CategoriaContabilidadDB


class CategoriaContabilidadRepository(ICategoriaContabilidadRepository):
    """Implementación de repositorio utilizando SQLAlchemy."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def create(
        self, categoria: CategoriaContabilidadCreate
    ) -> CategoriaContabilidad:
        db_categoria = CategoriaContabilidadDB(
            nombre=categoria.nombre,
            codigo=categoria.codigo,
        )

        try:
            self._db.add(db_categoria)
            self._db.commit()
            self._db.refresh(db_categoria)
        except SQLAlchemyError as exc:  # pragma: no cover - manejo de errores DB
            self._db.rollback()
            raise exc

        return CategoriaContabilidad.model_validate(db_categoria)
