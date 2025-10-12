from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from config import get_db
from domain.services.categoria_contabilidad_service import (
    CategoriaContabilidadService,
)
from domain.services.interfaces.categoria_contabilidad_service import (
    ICategoriaContabilidadService,
)
from infrastructure.repository.categoria_contabilidad_repository import (
    CategoriaContabilidadRepository,
)


def get_categoria_contabilidad_service(
    db: Session = Depends(get_db),
) -> ICategoriaContabilidadService:
    try:
        repository = CategoriaContabilidadRepository(db)
        return CategoriaContabilidadService(repository)
    except Exception as exc:  # pragma: no cover - inicialización crítica
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No se pudo inicializar el servicio de categorías contables: {exc}",
        ) from exc
