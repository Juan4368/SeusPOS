from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Literal

from pydantic import BaseModel, Field, field_validator


_ALLOWED_TIPO_INGRESO = ("efectivo", "transferencia")


class IngresoCreate(BaseModel):
    """Datos necesarios para registrar un ingreso."""

    monto: Decimal = Field(..., gt=0, max_digits=10)
    categoria_contabilidad_id: int | None = Field(
        default=None,
        gt=0,
        description="Identificador de la categoría contable asociada al ingreso.",
    )
    fecha: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Fecha del ingreso. Si no se envía se usa la hora actual en UTC.",
    )
    notas: str | None = Field(
        default=None,
        max_length=255,
        description="Notas adicionales sobre el ingreso.",
    )
    cliente: str | None = Field(
        default=None,
        max_length=150,
        description="Nombre del cliente asociado al ingreso, si aplica.",
    )
    tipo_ingreso: Literal["efectivo", "transferencia"] = Field(
        ..., description="Medio por el cual se recibió el ingreso."
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "monto": "150000.00",
                    "categoria_contabilidad_id": 2,
                    "fecha": "2024-01-10T15:30:00Z",
                    "notas": "Pago factura 123",
                    "cliente": "Juan Pérez",
                    "tipo_ingreso": "transferencia",
                }
            ]
        },
    }

    @field_validator("monto")
    @classmethod
    def normalizar_monto(cls, value: Decimal) -> Decimal:
        """Normaliza el monto a dos decimales con redondeo bancario."""
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

    @field_validator("tipo_ingreso")
    @classmethod
    def validar_tipo_ingreso(cls, value: str) -> str:
        if value not in _ALLOWED_TIPO_INGRESO:
            raise ValueError(
                "Tipo de ingreso inválido. Valores permitidos: 'efectivo' o 'transferencia'."
            )
        return value

    @field_validator("notas", "cliente")
    @classmethod
    def limpiar_texto(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None


class IngresoResponse(BaseModel):
    """Respuesta estándar para operaciones que devuelven un ingreso."""

    ingreso_id: int
    monto: Decimal
    categoria_contabilidad_id: int | None = None
    fecha: datetime
    notas: str | None = None
    cliente: str | None = None
    tipo_ingreso: str

    model_config = {
        "from_attributes": True,
    }
