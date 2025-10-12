from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.helpers.get_ingreso_service import get_ingreso_service
from domain.schemas.ingreso import IngresoCreate, IngresoResponse
from domain.services.interfaces.ingreso_service import IIngresoService

router = APIRouter(prefix="/ingresos", tags=["ingresos"])


@router.post("", response_model=IngresoResponse, status_code=status.HTTP_201_CREATED)
def registrar_ingreso(
    payload: IngresoCreate,
    service: IIngresoService = Depends(get_ingreso_service),
) -> IngresoResponse:
    try:
        ingreso = service.registrar_ingreso(payload)
        return IngresoResponse.model_validate(ingreso)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo registrar el ingreso por un conflicto de integridad.{exc}",
        ) from exc
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al persistir el ingreso en la base de datos.{exc}",
            

        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:  # pragma: no cover - error inesperado
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ha ocurrido un error inesperado al registrar el ingreso.",
        ) from exc
