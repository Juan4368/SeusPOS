from pydantic import BaseModel


class CategoriaContabilidad(BaseModel):
    id: int
    nombre: str
    codigo: str

    class Config:
        from_attributes = True
