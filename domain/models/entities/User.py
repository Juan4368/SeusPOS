from datetime import datetime

from pydantic import BaseModel

from .UserRole import UserRole


class User(BaseModel):
    user_id: int
    correo: str
    nombre_completo: str | None = None
    contrasena_hash: str
    role: UserRole
    activo: bool
    creado_at: datetime | None = None
    actualizado_at: datetime | None = None

    class Config:
        from_attributes = True
