from __future__ import annotations

from domain.interfaces.categoria_contabilidad_repository import (
    ICategoriaContabilidadRepository,
)
from domain.models.entities.CategoriaContabilidad import CategoriaContabilidad
from domain.schemas.categoria_contabilidad import CategoriaContabilidadCreate
from domain.services.interfaces.categoria_contabilidad_service import (
    ICategoriaContabilidadService,
)


class CategoriaContabilidadService(ICategoriaContabilidadService):
    """Servicio de dominio para la gestión de categorías contables."""

    def __init__(self, repository: ICategoriaContabilidadRepository) -> None:
        self._repository = repository

    def registrar_categoria(
        self, categoria: CategoriaContabilidadCreate
    ) -> CategoriaContabilidad:
        """Registra una categoría contable en el repositorio."""

        return self._repository.create(categoria)
