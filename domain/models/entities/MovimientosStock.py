from datetime import datetime

from pydantic import BaseModel


class MovimientosStock(BaseModel):
    movimiento_id: int
    stock_id: int
    producto_id: int
    tipo_movimiento_id: int
    ref_movimiento_id: int
    cantidad: int
    referencia_doc: str | None = None
    nota: str | None = None
    realizado_por_id: int
    fecha_creacion: datetime | None = None

    class Config:
        from_attributes = True
