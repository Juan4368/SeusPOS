from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Cartera(BaseModel):
    cartera_id: int
    monto: Decimal
    categoria_contabilidad_id: int | None = None
    fecha: datetime
    cliente: str | None = None
    notas: str | None = None

    class Config:
        from_attributes = True
