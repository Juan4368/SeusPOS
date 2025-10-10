from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class Product(BaseModel):
    producto_id: int
    codigo_barras: str
    nombre: str
    categoria_id: int
    descripcion: str | None = None
    precio_venta: Decimal
    costo: Decimal
    creado_por_id: int
    actualizado_por_id: int
    fecha_creacion: datetime | None = None
    fecha_actualizacion: datetime | None = None
    estado: bool

    class Config:
        from_attributes = True  # permite convertir desde objetos ORM


    
