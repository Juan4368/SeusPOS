from __future__ import annotations

from domain.interfaces.ingreso_repository import IIngresoRepository
from domain.models.entities.Ingreso import Ingreso
from domain.schemas.ingreso import IngresoCreate
from domain.services.interfaces.ingreso_service import IIngresoService


class IngresoService(IIngresoService):
    """Servicio de dominio para la gestión de ingresos."""

    def __init__(self, repository: IIngresoRepository) -> None:
        self._repository = repository

    def registrar_ingreso(self, ingreso: IngresoCreate) -> Ingreso:
        """Registra un ingreso garantizando las invariantes del dominio."""
        return self._repository.create(ingreso)
