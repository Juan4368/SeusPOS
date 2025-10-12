from __future__ import annotations

from typing import Protocol

from domain.models.entities.Egreso import Egreso
from domain.schemas.egreso import EgresoCreate


class IEgresoRepository(Protocol):
    """Contrato para la persistencia de egresos."""

    def create(self, egreso: EgresoCreate) -> Egreso:
        """Persiste un nuevo egreso y devuelve la entidad resultante."""
        ...
