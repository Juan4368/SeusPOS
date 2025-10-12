from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

from pydantic import BaseModel, Field, field_validator


class CarteraCreate(BaseModel):
    """Datos necesarios para registrar un movimiento de cartera."""

    monto: Decimal = Field(..., gt=0, max_digits=10)
    categoria_contabilidad_id: int | None = Field(
        default=None,
        gt=0,
        description="Identificador de la categoría contable asociada a la cartera.",
    )
    fecha: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Fecha del movimiento de cartera. Si no se envía se usa la hora actual en UTC.",
    )
    cliente: str | None = Field(
        default=None,
        max_length=150,
        description="Nombre del cliente asociado a la cartera.",
    )
    notas: str | None = Field(
        default=None,
        max_length=255,
        description="Notas adicionales sobre el movimiento.",
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "monto": "200000.00",
                    "categoria_contabilidad_id": 4,
                    "fecha": "2024-01-11T10:00:00Z",
                    "cliente": "Cliente ABC",
                    "notas": "Saldo pendiente factura 456",
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

    @field_validator("notas", "cliente")
    @classmethod
    def limpiar_texto(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None


class CarteraResponse(BaseModel):
    """Respuesta estándar para operaciones que devuelven una cartera."""

    cartera_id: int
    monto: Decimal
    categoria_contabilidad_id: int | None = None
    fecha: datetime
    cliente: str | None = None
    notas: str | None = None

    model_config = {
        "from_attributes": True,
    }
