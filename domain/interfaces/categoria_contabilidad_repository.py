from __future__ import annotations

from typing import Protocol

from domain.models.entities.CategoriaContabilidad import CategoriaContabilidad
from domain.schemas.categoria_contabilidad import CategoriaContabilidadCreate


class ICategoriaContabilidadRepository(Protocol):
    """Contrato que debe cumplir cualquier repositorio de categorías contables."""

    def create(
        self, categoria: CategoriaContabilidadCreate
    ) -> CategoriaContabilidad:
        """Persiste una nueva categoría y devuelve la entidad resultante."""
        ...
