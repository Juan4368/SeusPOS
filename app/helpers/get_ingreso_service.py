from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from config import get_db
from domain.services.ingreso_service import IngresoService
from domain.services.interfaces.ingreso_service import IIngresoService
from infrastructure.repository.ingreso_repository import IngresoRepository


def get_ingreso_service(db: Session = Depends(get_db)) -> IIngresoService:
    try:
        repository = IngresoRepository(db)
        return IngresoService(repository)
    except Exception as exc:  # pragma: no cover - inicialización crítica
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No se pudo inicializar el servicio de ingresos: {exc}",
        ) from exc
