from pydantic import BaseModel


class RefMovimiento(BaseModel):
    ref_movimiento_id: int
    nombre: str
    descripcion: str | None = None
    activo: bool

    class Config:
        from_attributes = True
