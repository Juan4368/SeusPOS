from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Literal

from pydantic import BaseModel, Field, field_validator

_ALLOWED_TIPO_EGRESO = ("efectivo", "transferencia")


class EgresoCreate(BaseModel):
    """Datos necesarios para registrar un egreso."""

    monto: Decimal = Field(..., gt=0, max_digits=10)
    categoria_contabilidad_id: int | None = Field(
        default=None,
        gt=0,
        description="Identificador de la categoría contable asociada al egreso.",
    )
    fecha: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Fecha del egreso. Si no se envía se usa la hora actual en UTC.",
    )
    notas: str | None = Field(
        default=None,
        max_length=255,
        description="Notas adicionales sobre el egreso.",
    )
    cliente: str | None = Field(
        default=None,
        max_length=150,
        description="Nombre del proveedor u otra contraparte asociada al egreso.",
    )
    tipo_egreso: Literal["efectivo", "transferencia"] = Field(
        ..., description="Medio por el cual se realizó el egreso."
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "monto": "50000.00",
                    "categoria_contabilidad_id": 3,
                    "fecha": "2024-01-10T15:30:00Z",
                    "notas": "Pago de servicios",
                    "cliente": "Proveedor XYZ",
                    "tipo_egreso": "transferencia",
                }
            ]
        },
    }

    @field_validator("monto")
    @classmethod
    def normalizar_monto(cls, value: Decimal) -> Decimal:
        cuantizado = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if cuantizado <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        return cuantizado

    @field_validator("fecha")
    @classmethod
    def asegurar_timezone(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @field_validator("tipo_egreso")
    @classmethod
    def validar_tipo_egreso(cls, value: str) -> str:
        if value not in _ALLOWED_TIPO_EGRESO:
            raise ValueError(
                "Tipo de egreso inválido. Valores permitidos: 'efectivo' o 'transferencia'."
            )
        return value

    @field_validator("notas", "cliente")
    @classmethod
    def limpiar_texto(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None


class EgresoResponse(BaseModel):
    """Respuesta estándar para operaciones que devuelven un egreso."""

    egreso_id: int
    monto: Decimal
    categoria_contabilidad_id: int | None = None
    fecha: datetime
    notas: str | None = None
    cliente: str | None = None
    tipo_egreso: str

    model_config = {
        "from_attributes": True,
    }
