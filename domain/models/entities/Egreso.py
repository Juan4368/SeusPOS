from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Egreso(BaseModel):
    egreso_id: int
    monto: Decimal
    categoria_id: int | None = None
    fecha: datetime
    notas: str | None = None
    cliente: str | None = None
    tipo_egreso: str

    class Config:
        from_attributes = True
