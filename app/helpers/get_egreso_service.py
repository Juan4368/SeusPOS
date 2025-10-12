from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from config import get_db
from domain.services.egreso_service import EgresoService
from domain.services.interfaces.egreso_service import IEgresoService
from infrastructure.repository.egreso_repository import EgresoRepository


def get_egreso_service(db: Session = Depends(get_db)) -> IEgresoService:
    try:
        repository = EgresoRepository(db)
        return EgresoService(repository)
    except Exception as exc:  # pragma: no cover - inicialización crítica
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No se pudo inicializar el servicio de egresos: {exc}",
        ) from exc
