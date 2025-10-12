from __future__ import annotations

from domain.interfaces.cartera_repository import ICarteraRepository
from domain.models.entities.Cartera import Cartera
from domain.schemas.cartera import CarteraCreate
from domain.services.interfaces.cartera_service import ICarteraService


class CarteraService(ICarteraService):
    """Servicio de dominio para la gestión de cartera."""

    def __init__(self, repository: ICarteraRepository) -> None:
        self._repository = repository

    def registrar_cartera(self, cartera: CarteraCreate) -> Cartera:
        """Registra un movimiento de cartera aplicando las reglas del dominio."""
        return self._repository.create(cartera)
