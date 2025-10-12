from __future__ import annotations

from typing import Protocol

from domain.models.entities.Cartera import Cartera
from domain.schemas.cartera import CarteraCreate


class ICarteraRepository(Protocol):
    """Contrato para la persistencia de cuentas por cobrar (cartera)."""

    def create(self, cartera: CarteraCreate) -> Cartera:
        """Persiste un nuevo registro de cartera y devuelve la entidad resultante."""
        ...
