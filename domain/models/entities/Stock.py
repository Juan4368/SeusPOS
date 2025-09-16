from datetime import datetime

from pydantic import BaseModel


class Stock(BaseModel):
    stock_id: int
    producto_id: int
    cantidad_actual: int
    cantidad_minima: int
    ultima_actualizacion: datetime | None = None

    class Config:
        from_attributes = True
