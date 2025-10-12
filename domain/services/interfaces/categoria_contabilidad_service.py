from __future__ import annotations

from typing import Protocol

from domain.models.entities.CategoriaContabilidad import CategoriaContabilidad
from domain.schemas.categoria_contabilidad import CategoriaContabilidadCreate


class ICategoriaContabilidadService(Protocol):
    """Definición del servicio de categorías contables."""

    def registrar_categoria(
        self, categoria: CategoriaContabilidadCreate
    ) -> CategoriaContabilidad:
        ...
