from __future__ import annotations

from domain.interfaces.egreso_repository import IEgresoRepository
from domain.models.entities.Egreso import Egreso
from domain.schemas.egreso import EgresoCreate
from domain.services.interfaces.egreso_service import IEgresoService


class EgresoService(IEgresoService):
    """Servicio de dominio para la gestión de egresos."""

    def __init__(self, repository: IEgresoRepository) -> None:
        self._repository = repository

    def registrar_egreso(self, egreso: EgresoCreate) -> Egreso:
        """Registra un egreso aplicando las reglas del dominio."""
        return self._repository.create(egreso)
