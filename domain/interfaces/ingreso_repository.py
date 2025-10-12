from __future__ import annotations

from typing import Protocol

from domain.models.entities.Ingreso import Ingreso
from domain.schemas.ingreso import IngresoCreate


class IIngresoRepository(Protocol):
    """Contrato que debe cumplir cualquier repositorio de ingresos."""

    def create(self, ingreso: IngresoCreate) -> Ingreso:
        """Persiste un nuevo ingreso y devuelve la entidad resultante."""
        ...
