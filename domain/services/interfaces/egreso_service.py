from __future__ import annotations

from typing import Protocol

from domain.models.entities.Egreso import Egreso
from domain.schemas.egreso import EgresoCreate


class IEgresoService(Protocol):
    """Definición del servicio de egresos."""

    def registrar_egreso(self, egreso: EgresoCreate) -> Egreso:
        ...
