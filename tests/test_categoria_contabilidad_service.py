from unittest.mock import MagicMock

import pytest

from domain.models.entities.CategoriaContabilidad import CategoriaContabilidad
from domain.schemas.categoria_contabilidad import CategoriaContabilidadCreate
from domain.services.categoria_contabilidad_service import (
    CategoriaContabilidadService,
)


@pytest.fixture()
def categoria_create() -> CategoriaContabilidadCreate:
    return CategoriaContabilidadCreate(nombre="Ingresos varios", codigo="ing-var")


@pytest.fixture()
def categoria_entity() -> CategoriaContabilidad:
    return CategoriaContabilidad(id=1, nombre="Ingresos varios", codigo="ING-VAR")


def test_registrar_categoria_devuelve_entidad(
    categoria_create: CategoriaContabilidadCreate,
    categoria_entity: CategoriaContabilidad,
) -> None:
    repository = MagicMock()
    repository.create.return_value = categoria_entity

    service = CategoriaContabilidadService(repository)

    result = service.registrar_categoria(categoria_create)

    repository.create.assert_called_once_with(categoria_create)
    assert isinstance(result, CategoriaContabilidad)
    assert result.codigo == "ING-VAR"
