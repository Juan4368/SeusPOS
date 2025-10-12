from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from config import get_db
from domain.services.cartera_service import CarteraService
from domain.services.interfaces.cartera_service import ICarteraService
from infrastructure.repository.cartera_repository import CarteraRepository


def get_cartera_service(db: Session = Depends(get_db)) -> ICarteraService:
    try:
        repository = CarteraRepository(db)
        return CarteraService(repository)
    except Exception as exc:  # pragma: no cover - inicialización crítica
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No se pudo inicializar el servicio de cartera: {exc}",
        ) from exc
