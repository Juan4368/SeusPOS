from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from domain.interfaces.ingreso_repository import IIngresoRepository
from domain.models.entities.Ingreso import Ingreso
from domain.schemas.ingreso import IngresoCreate
from domain.services.ingreso_service import IngresoService


def test_registrar_ingreso_delega_en_repositorio():
    repo_mock: IIngresoRepository = MagicMock()
    service = IngresoService(repo_mock)

    payload = IngresoCreate(
        monto=Decimal("100.00"),
        categoria_contabilidad_id=1,
        fecha=datetime(2024, 1, 1, tzinfo=timezone.utc),
        notas="Pago en efectivo",
        cliente="Cliente Demo",
        tipo_ingreso="efectivo",
    )

    ingreso_creado = Ingreso(
        ingreso_id=1,
        monto=payload.monto,
        categoria_contabilidad_id=payload.categoria_contabilidad_id,
        fecha=payload.fecha,
        notas=payload.notas,
        cliente=payload.cliente,
        tipo_ingreso=payload.tipo_ingreso,
    )

    repo_mock.create.return_value = ingreso_creado

    resultado = service.registrar_ingreso(payload)

    repo_mock.create.assert_called_once_with(payload)
    assert resultado == ingreso_creado


def test_ingreso_create_normaliza_y_valida_datos():
    payload = IngresoCreate(
        monto=Decimal("100.005"),
        categoria_contabilidad_id=2,
        fecha=datetime(2024, 2, 2, 10, 0, 0),
        notas="  Nota con espacios  ",
        cliente="  Cliente  ",
        tipo_ingreso="transferencia",
    )

    assert payload.monto == Decimal("100.01")
    assert payload.fecha.tzinfo == timezone.utc
    assert payload.notas == "Nota con espacios"
    assert payload.cliente == "Cliente"


@pytest.mark.parametrize("tipo_ingreso", ["tarjeta", "", None])
def test_ingreso_create_rechaza_tipo_ingreso_invalido(tipo_ingreso):
    with pytest.raises(ValueError):
        IngresoCreate(
            monto=Decimal("1"),
            tipo_ingreso=tipo_ingreso,  # type: ignore[arg-type]
        )
