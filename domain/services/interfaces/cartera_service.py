from __future__ import annotations

from typing import Protocol

from domain.models.entities.Cartera import Cartera
from domain.schemas.cartera import CarteraCreate


class ICarteraService(Protocol):
    """Definición del servicio de cartera."""

    def registrar_cartera(self, cartera: CarteraCreate) -> Cartera:
        ...
