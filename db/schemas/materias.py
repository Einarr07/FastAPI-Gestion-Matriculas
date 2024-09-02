from pydantic import BaseModel, Field

class CrearMateria(BaseModel):
    nombre: str
    codigo: int
    descripcion: str = Field(..., max_length=200)
    creditos: int

    class Config:
        from_attributes = True

class ObtenerMateria(BaseModel):
    id: int
    nombre: str
    codigo: int
    descripcion: str
    creditos: int

class ActualizarMatria(BaseModel):
    nombre: str
    codigo: int
    descripcion: str = Field(..., max_length=200)
    creditos: int

    class Config:
        from_attributes = True

class EliminarMateria(BaseModel):
    mensaje: str
    