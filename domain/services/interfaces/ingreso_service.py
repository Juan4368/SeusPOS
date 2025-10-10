from __future__ import annotations

from typing import Protocol

from domain.models.entities.Ingreso import Ingreso
from domain.schemas.ingreso import IngresoCreate


class IIngresoService(Protocol):
    """Definición del servicio de ingresos."""

    def registrar_ingreso(self, ingreso: IngresoCreate) -> Ingreso:
        ...
