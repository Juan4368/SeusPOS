from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.helpers.get_cartera_service import get_cartera_service
from domain.schemas.cartera import CarteraCreate, CarteraResponse
from domain.services.interfaces.cartera_service import ICarteraService

router = APIRouter(prefix="/carteras", tags=["carteras"])


@router.post("", response_model=CarteraResponse, status_code=status.HTTP_201_CREATED)
def registrar_cartera(
    payload: CarteraCreate,
    service: ICarteraService = Depends(get_cartera_service),
) -> CarteraResponse:
    try:
        cartera = service.registrar_cartera(payload)
        return CarteraResponse.model_validate(cartera)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo registrar la cartera por un conflicto de integridad.{exc}",
        ) from exc
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al persistir la cartera en la base de datos.{exc}",
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:  # pragma: no cover - error inesperado
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ha ocurrido un error inesperado al registrar la cartera.",
        ) from exc
