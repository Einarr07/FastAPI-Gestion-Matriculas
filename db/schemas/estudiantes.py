from pydantic import BaseModel, EmailStr, validator, Field
from datetime import date, datetime

class CrearEstudiante(BaseModel):
    nombre: str
    apellido: str
    cedula: str = Field(..., min_length=10, max_length=10)
    fecha_nacimiento: date
    ciudad: str
    direccion: str
    telefono: str = Field(..., min_length=10, max_length=10)
    email: EmailStr

    @validator("fecha_nacimiento", pre=True, always=True)
    def analizar_fecha(cls, value):
        if isinstance(value, date):
            return value
        elif isinstance(value, str):
            return datetime.strptime(value, "%d-%m-%Y").date()
        else:
            raise ValueError("El formato de fehca no es válido")

    class Config:
        from_attributes = True

class ObtenerEstudiante(BaseModel):
    id: int
    nombre: str
    apellido: str
    cedula: int
    fecha_nacimiento: date
    ciudad: str
    direccion: str
    telefono: str
    email: EmailStr

class ActualizarEstudiante(BaseModel):
    nombre: str
    apellido: str
    cedula: str = Field(..., min_length=10, max_length=10)
    fecha_nacimiento: date
    ciudad: str
    direccion: str
    telefono: str = Field(..., min_length=10, max_length=10)
    email: EmailStr

    @validator("fecha_nacimiento", pre=True, always=True)
    def analizar_fecha(cls, value):
        if isinstance(value, date):
            return value
        elif isinstance(value, str):
            return datetime.strptime(value, "%d-%m-%Y").date()
        else:
            raise ValueError("El formato de fehca no es válido")

    class Config:
        from_attributes = True

class EliminarEstudiante(BaseModel):
    mensaje: str