from datetime import datetime

from pydantic import BaseModel


class Categoria(BaseModel):
    categoria_id: int
    nombre: str
    descripcion: str | None = None
    estado: bool
    fecha_creacion: datetime | None = None
    fecha_actualizacion: datetime | None = None

    class Config:
        from_attributes = True
