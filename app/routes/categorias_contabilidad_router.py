from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.helpers.get_categoria_contabilidad_service import (
    get_categoria_contabilidad_service,
)
from domain.schemas.categoria_contabilidad import (
    CategoriaContabilidadCreate,
    CategoriaContabilidadResponse,
)
from domain.services.interfaces.categoria_contabilidad_service import (
    ICategoriaContabilidadService,
)

router = APIRouter(prefix="/categorias-contabilidad", tags=["categorias_contabilidad"])


@router.post("", response_model=CategoriaContabilidadResponse, status_code=status.HTTP_201_CREATED)
def registrar_categoria_contable(
    payload: CategoriaContabilidadCreate,
    service: ICategoriaContabilidadService = Depends(get_categoria_contabilidad_service),
) -> CategoriaContabilidadResponse:
    try:
        categoria = service.registrar_categoria(payload)
        return CategoriaContabilidadResponse.model_validate(categoria)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo registrar la categoría contable por un conflicto de integridad.",
        ) from exc
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al persistir la categoría contable en la base de datos.",
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:  # pragma: no cover - error inesperado
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ha ocurrido un error inesperado al registrar la categoría contable.",
        ) from exc
