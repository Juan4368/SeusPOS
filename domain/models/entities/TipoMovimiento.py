from pydantic import BaseModel


class TipoMovimiento(BaseModel):
    tipo_movimiento_id: int
    nombre: str
    descripcion: str | None = None
    activo: bool

    class Config:
        from_attributes = True
