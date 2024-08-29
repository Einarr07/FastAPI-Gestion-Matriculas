from pydantic import BaseModel, Field, EmailStr

class CrearUsuario(BaseModel):
    id: str = Field(..., min_length=11, max_length=11)
    nombre: str
    apellido: str
    email: EmailStr
    password: str
    id_estudiante: int | None = None # Opcional

class ObtenerUsuario(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: EmailStr

    class Config:
        from_attributes = True

class CredencialesUsuario(BaseModel):
    email: EmailStr = Field(..., min_length=1)
    password: str = Field(..., min_length=1)