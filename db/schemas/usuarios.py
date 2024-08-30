from pydantic import BaseModel, Field, EmailStr

class CrearUsuario(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    password: str = Field(..., min_length=8)

class ObtenerUsuario(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: EmailStr

    class Config:
        from_attributes = True

class CredencialesUsuario(BaseModel):
    email: EmailStr = Field(..., min_length=1)
    password: str = Field(..., min_length=8)