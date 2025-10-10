from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Ingreso(BaseModel):
    ingreso_id: int
    monto: Decimal
    categoria_contabilidad_id: int | None = None
    fecha: datetime
    notas: str | None = None
    cliente: str | None = None
    tipo_ingreso: str

    class Config:
        from_attributes = True
