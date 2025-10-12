from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.helpers.get_egreso_service import get_egreso_service
from domain.schemas.egreso import EgresoCreate, EgresoResponse
from domain.services.interfaces.egreso_service import IEgresoService

router = APIRouter(prefix="/egresos", tags=["egresos"])


@router.post("", response_model=EgresoResponse, status_code=status.HTTP_201_CREATED)
def registrar_egreso(
    payload: EgresoCreate,
    service: IEgresoService = Depends(get_egreso_service),
) -> EgresoResponse:
    try:
        egreso = service.registrar_egreso(payload)
        return EgresoResponse.model_validate(egreso)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo registrar el egreso por un conflicto de integridad.{exc}",
        ) from exc
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al persistir el egreso en la base de datos.{exc}",
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:  # pragma: no cover - error inesperado
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ha ocurrido un error inesperado al registrar el egreso.",
        ) from exc
