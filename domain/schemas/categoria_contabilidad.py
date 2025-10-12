from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class CategoriaContabilidadCreate(BaseModel):
    """Datos necesarios para registrar una categoría contable."""

    nombre: str = Field(
        ..., min_length=1, max_length=100, description="Nombre legible de la categoría"
    )
    codigo: str = Field(
        ..., min_length=1, max_length=50, description="Código único de referencia"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "Ventas locales",
                    "codigo": "VENT-LOC",
                }
            ]
        }
    }

    @field_validator("nombre", "codigo")
    @classmethod
    def limpiar_cadena(cls, value: str) -> str:
        limpio = value.strip()
        if not limpio:
            raise ValueError("El campo no puede estar vacío")
        return limpio

    @field_validator("codigo")
    @classmethod
    def normalizar_codigo(cls, value: str) -> str:
        return value.upper()


class CategoriaContabilidadResponse(BaseModel):
    """Respuesta para operaciones relacionadas con categorías contables."""

    id: int
    nombre: str
    codigo: str

    model_config = {"from_attributes": True}
